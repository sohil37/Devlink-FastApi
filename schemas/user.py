from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from enums.user import GenderEnum

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    id: int
    created_at: datetime
    message: str
    class Config:
        from_attributes = True

# ----------------------
# UserAddress Schema
# ----------------------
class UserAddressBase(BaseModel):
    user_id: int
    line_1: str
    line_2: str
    city: str
    postal_code: str
    state: str
    country: str

class UserAddressCreate(UserAddressBase):
    pass

class UserAddressUpdate():
    user_id: int
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class UserAddressResponse(UserAddressBase):
    id: int
    message: str
    class Config:
        from_attributes = True

# ----------------------
# UserProfile Schema
# ----------------------
class UserProfileBase(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    phone_no: Optional[str] = None
    dob: Optional[date] = None
    address_id: Optional[int] = None
    profile_picture_url: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    message: str
    class Config:
        from_attributes = True