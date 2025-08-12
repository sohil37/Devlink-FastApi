from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from deps.auth import get_user_id_from_access_token
from schemas.user import UserProfileBase, UserProfileResponse
from models.user import UserProfile
from services.user_services import get_profile_by_user_id

router = APIRouter()

@router.post("/upsert_profile", response_model=UserProfileResponse)
def upsert_profile(
    payload: UserProfileBase,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id_from_access_token)
):
    try:
        profile = get_profile_by_user_id(db=db, user_id=user_id)
        if profile:
            # Update only the fields provided in payload
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(profile, key, value)
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