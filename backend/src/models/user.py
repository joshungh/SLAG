from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class LoginMethod(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    WEB3 = "web3"

class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    login_methods: List[LoginMethod] = []
    web3_wallet: Optional[str] = None
    created_at: Optional[str] = None
    author_metadata: Optional[Dict] = Field(default_factory=dict)
    last_login: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    web3_wallet: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    login_method: LoginMethod

class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    web3_wallet: Optional[str] = None
    google_token: Optional[str] = None
    login_method: LoginMethod

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    author_metadata: Optional[Dict] = None

class UserResponse(UserBase):
    pass 