from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class Usuario(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


class UsuarioResponse(BaseModel):
    id: int
    name: str
    role: str

class UsuarioUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None
    role: Literal["admin", "support", "user"] | None = None
    is_active: bool | None = None
