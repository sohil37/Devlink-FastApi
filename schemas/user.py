from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    id: int
    created_at: datetime
    message: str
    class Config:
        from_attributes = True