from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.security import get_current_user
from app.models.user_model import User

from app.config.limiter import limiter

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse
)

from app.dependencies.database_dependency import get_db

from app.auth.auth_service import (
    register_user,
    authenticate_user,
    login_user
)

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router_auth.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    user = register_user(
        db,
        user_data
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado."
        )

    return user


@router_auth.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos."
        )

    return login_user(user)


@router_auth.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user