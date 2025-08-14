from typing import Optional
from pydantic import BaseModel
from datetime import date
from enums.user import GenderEnum
from schemas.base import AtLeastOneFieldRequiredMixin

# ----------------------
# UserProfile Schema
# ----------------------
class UserProfileBase(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    gender: Optional[GenderEnum] = None
    phone_no: Optional[str] = ""
    dob: Optional[date] = None
    profile_picture_url: Optional[str] = ""

class UpdateUserProfilePayload(AtLeastOneFieldRequiredMixin, UserProfileBase):
    pass

class UserProfileResponse(BaseModel):
    id: int
    message: str
    class Config:
        from_attributes = True