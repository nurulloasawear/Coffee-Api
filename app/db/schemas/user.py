from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password:str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
class UserResponse(UserBase):
    id: int
    is_verified: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True 
class UserAdminUpdate(BaseModel):
    role: Optional[str] = None
    is_verified: Optional[bool] = None