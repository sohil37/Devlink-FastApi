from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from enums.user import GenderEnum
from schemas.base import AtLeastOneFieldRequiredMixin

class UserCreateResponse(BaseModel):
    id: int
    created_at: datetime
    message: str
    class Config:
        from_attributes = True

# ----------------------
# UserProfile Schema
# ----------------------
class UserProfileBase(AtLeastOneFieldRequiredMixin, BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    phone_no: Optional[str] = None
    dob: Optional[date] = None
    address_id: Optional[int] = None
    profile_picture_url: Optional[str] = None

class UserProfileUpdate(UserProfileBase):
    user_id: int

class UserProfileResponse(BaseModel):
    id: int
    message: str
    class Config:
        from_attributes = True

# ----------------------
# UserAddress Schema
# ----------------------
class UserAddressBase(BaseModel):
    line_1: str
    line_2: str
    city: str
    postal_code: str
    state: str
    country: str

class UserAddressUpdate(UserAddressBase):
    user_id: int

class UserAddressResponse(BaseModel):
    id: int
    message: str
    class Config:
        from_attributes = True