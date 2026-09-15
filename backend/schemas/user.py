from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    signup_type: str
    team_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str