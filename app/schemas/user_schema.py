from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    SALON_ADMIN = "salon_admin"
    CUSTOMER = "customer"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: str = Field(..., min_length=10, max_length=15)
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    userType: "UserRole"
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    otp: Optional[str] = None