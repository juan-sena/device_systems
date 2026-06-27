import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(...)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios.")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Debe contener al menos una mayúscula.")

        if not re.search(r"[a-z]", value):
            raise ValueError("Debe contener al menos una minúscula.")

        if not re.search(r"\d", value):
            raise ValueError("Debe contener al menos un número.")

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)