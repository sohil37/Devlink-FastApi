from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.utils import update_fields_on_obj
from db.session import get_db
from deps.auth import get_user_id_from_access_token
from models.user import UserProfile, UserAddress
from schemas.user.user_address import UserAddressResponse, UpdateUserAddressPayload, UserAddressBase
from schemas.user.user_profile import UpdateUserProfilePayload, UserProfileResponse, UserProfileBase
from services.user_services import get_profile_by_user_id, get_address_by_user_id

router = APIRouter()

# ------------------------------
# Profile APIs
# ------------------------------
@router.patch("/update_profile", response_model=UserProfileResponse)
def update_profile(
    payload: UpdateUserProfilePayload,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id_from_access_token)
):
    try:
        profile = get_profile_by_user_id(db=db, user_id=user_id)
        if profile:
            # Update only the fields provided in payload
            update_fields_on_obj(obj=profile, dict_to_update=payload.model_dump(exclude_unset=True))
        else:
            # Create a new profile
            profile = UserProfile(**payload.model_dump(), user_id=user_id)
            db.add(profile)
        db.commit()
        db.refresh(profile)
        return UserProfileResponse(id=profile.id, message="Profile updated successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/get_profile", response_model=UserProfileBase)
def get_profile(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_id_from_access_token)
):
    profile = get_profile_by_user_id(db=db, user_id=user_id)
    if profile:
        return UserProfileBase(**profile.__dict__)
    else:
        return UserProfileBase()

@router.put("/update_address", response_model=UserAddressResponse)
def update_address(
    payload: UpdateUserAddressPayload,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id_from_access_token)
):
    try:
        address = get_address_by_user_id(db=db, user_id=user_id)
        if address:
            # Update all fields from payload
            update_fields_on_obj(obj=address, dict_to_update=payload.model_dump())
        else:
            # Create a new address
            address = UserAddress(**payload.model_dump(), user_id=user_id)
            db.add(address)
        db.commit()
        db.refresh(address)
        return UserAddressResponse(id=address.id, message="Address updated successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/get_address", response_model=UserAddressBase)
def get_address(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_id_from_access_token)
):
    address = get_address_by_user_id(db=db, user_id=user_id)
    if address:
        return UserAddressBase(**address.__dict__)
    else:
        return UserAddressBase()