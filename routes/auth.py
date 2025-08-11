from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.user_services import get_user_by_email
from core.auth import verify_password, create_access_token, get_password_hash
from db.session import get_db
from models.user import User
from schemas.user import UserCredentials, UserCreateResponse
from schemas.auth import Token

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def register(credentials: UserCredentials, db: Session = Depends(get_db)):
    user = get_user_by_email(db, credentials.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(credentials.password)
    user = User(email=credentials.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserCreateResponse(id=user.id, created_at=user.created_at, message="User registered successfully")

@router.post("/login", response_model=Token)
async def login(
    credentials: UserCredentials,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(
        data={"sub": user.id}
    ) 
    return Token(access_token=access_token, token_type= "bearer")