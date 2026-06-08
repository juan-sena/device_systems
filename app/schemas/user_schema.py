from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }