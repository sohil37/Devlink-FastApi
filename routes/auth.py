from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Form
from sqlalchemy.orm import Session
from deps.auth import get_user_id_from_access_token
from schemas.user.user import UserCreateResponse
from schemas.user.user_address import UserAddressBase
from schemas.user.user_profile import UserProfileBase
from services.user_services import get_user_by_email, get_user_by_id
from core.auth import verify_password, create_access_token, create_refresh_token, decode_token, get_password_hash
from db.session import get_db
from models.user import User, UserProfile, UserAddress
from schemas.auth import TokenWithUserInfo
from core import config

router = APIRouter()

# ------------------------------
# Helper: issue new tokens & set cookie
# ------------------------------
def send_tokens_with_user_info(user: User, db: Session, response: Response) -> TokenWithUserInfo:
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    user.refresh_token = refresh_token
    db.commit()
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=False  # True in prod with HTTPS
    )
    return TokenWithUserInfo(access_token=access_token, token_type="bearer", user_id=user.id, email=user.email)

# ------------------------------
# Register
# ------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if get_user_by_email(db, username):
        raise HTTPException(status_code=400, detail="Email already registered")
    # Add user to User table
    user = User(email=username, password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Add empty profile to UserProfile table
    user_profile = UserProfile(**UserProfileBase().__dict__, user_id=user.id)
    db.add(user_profile)
    # Add empty address to UserAddress table
    user_address = UserAddress(**UserAddressBase().__dict__, user_id=user.id)
    db.add(user_address)
    db.commit()
    return UserCreateResponse(id=user.id, created_at=user.created_at, message="User registered successfully")

# ------------------------------
# Login
# ------------------------------
@router.post("/login", response_model=TokenWithUserInfo)
def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return send_tokens_with_user_info(user, db, response)

# ------------------------------
# Refresh token
# ------------------------------
@router.get("/refresh_token", response_model=TokenWithUserInfo)
async def refresh_token(response: Response, db: Session = Depends(get_db), refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    try:
        payload = decode_token(refresh_token, config.REFRESH_TOKEN_SECRET_KEY)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        user = get_user_by_id(db, user_id)
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        return send_tokens_with_user_info(user, db, response)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


# ------------------------------
# Logout
# ------------------------------
@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        # No cookie means already logged out
        return {"message": "Logged out successfully"}
    try:
        # Remove refresh token from DB
        payload = decode_token(refresh_token, config.REFRESH_TOKEN_SECRET_KEY)
        user_id = payload.get("sub")
        user = get_user_by_id(db, user_id)
        if user:
            user.refresh_token = None
            db.commit()
    except Exception(BaseException):
        # Ignore decoding errors (token might already be invalid/expired)
        pass
    # Clear refresh token from cookie
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="strict",
        secure=False  # True in production
    )
    return {"message": "Logged out successfully"}

# ------------------------------
# Delete Account
# ------------------------------
@router.delete("/delete_account", status_code=status.HTTP_200_OK)
async def delete_account(
    response: Response,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id_from_access_token)
):
    user = get_user_by_id(db=db, user_id=user_id)
    db.delete(user)
    db.commit()
    return {"message": "Account deleted successfully"}