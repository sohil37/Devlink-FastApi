from datetime import datetime
from pydantic import BaseModel

# ----------------------
# User Schema
# ----------------------
class UserCreateResponse(BaseModel):
    id: int
    created_at: datetime
    message: str
    class Config:
        from_attributes = True