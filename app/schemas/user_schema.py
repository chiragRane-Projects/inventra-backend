from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "staff"
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str