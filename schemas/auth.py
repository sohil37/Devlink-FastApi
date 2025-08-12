from pydantic import BaseModel, EmailStr

class TokenWithUserInfo(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: EmailStr