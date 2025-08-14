from typing import Optional
from pydantic import BaseModel

# ----------------------
# UserAddress Schema
# ----------------------
class UserAddressBase(BaseModel):
    line_1: Optional[str] = ""
    line_2: Optional[str] = ""
    city: Optional[str] = ""
    postal_code: Optional[str] = ""
    state: Optional[str] = ""
    country: Optional[str] = ""

class UpdateUserAddressPayload(UserAddressBase):
    line_1: str
    line_2: str
    city: str
    postal_code: str
    state: str
    country: str

class UserAddressResponse(BaseModel):
    id: int
    message: str
    class Config:
        from_attributes = True