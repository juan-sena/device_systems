from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.dependencies.database_dependency import get_db

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    patch_user,
    delete_user
)

router_user = APIRouter()


@router_user.get(
    "/users",
    response_model=list[UserResponse]
)
def obtener_usuarios(
    db: Session = Depends(get_db)
):
    return get_users(db)


@router_user.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def obtener_usuario_por_id(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router_user.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def crear_usuario(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    return create_user(
        db,
        user_data
    )


@router_user.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def actualizar_usuario(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if (
        existing_user
        and existing_user.id != user_id
    ):
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    return update_user(
        db,
        user,
        user_data
    )


@router_user.patch(
    "/users/{user_id}",
    response_model=UserResponse
)
def actualizar_usuario_parcial(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    datos_actualizados = user_data.model_dump(
        exclude_unset=True
    )

    if not datos_actualizados:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    if "email" in datos_actualizados:

        existing_user = get_user_by_email(
            db,
            datos_actualizados["email"]
        )

        if (
            existing_user
            and existing_user.id != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    return patch_user(
        db,
        user,
        datos_actualizados
    )


@router_user.delete(
    "/users/{user_id}",
    status_code=204
)
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    delete_user(
        db,
        user
    )

    return