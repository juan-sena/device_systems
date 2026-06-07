from fastapi import APIRouter, HTTPException, Response, Depends
from app.schemas.user_schema import Usuario, UsuarioResponse, UsuarioUpdate
from app.dependencies.user_dependencies import get_user_or_404
from app.data.users_db import usuarios

router_user = APIRouter()

# GET users
@router_user.get("/users")
def obtener_usuarios(
    role: str = None,
    is_active: bool = None
):

    resultado = usuarios

    if role is not None:
        resultado = [
            usuario for usuario in resultado
            if usuario.role == role
        ]

    if is_active is not None:
        resultado = [
            usuario for usuario in resultado
            if usuario.is_active == is_active
        ]

    return resultado


# GET user by id
@router_user.get("/users/{user_id}")
def obtener_usuario_por_id(
    usuario = Depends(get_user_or_404)
):
    return usuario


# POST users
@router_user.post("/users", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    usuario: Usuario,
    response: Response
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    
    for u in usuarios:
        if u.email == usuario.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    usuarios.append(usuario)

    return usuario


# PUT user
@router_user.put("/users/{user_id}")
def actualizar_usuario(
    user_id: int,
    usuario: Usuario
):

    for i, u in enumerate(usuarios):

        if u.id == user_id:

           
            for other in usuarios:
                if (
                    other.email == usuario.email
                    and other.id != user_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="El correo ya existe"
                    )

         
            usuarios[i] = usuario
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

#Actualizacion parcial del usuario
@router_user.patch("/users/{user_id}")
def actualizar_usuario_parcial(
    user_id: int,
    usuario: UsuarioUpdate
):

    datos_actualizados = usuario.model_dump(
        exclude_unset=True
    )

    if not datos_actualizados:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    for u in usuarios:

        if u.id == user_id:

            # Validar email duplicado solo si se envió email
            if "email" in datos_actualizados:

                for other in usuarios:

                    if (
                        other.email == datos_actualizados["email"]
                        and other.id != user_id
                    ):
                        raise HTTPException(
                            status_code=400,
                            detail="El correo ya existe"
                        )

            # Actualizar solo los campos enviados
            for campo, valor in datos_actualizados.items():
                setattr(u, campo, valor)

            return u

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

#Delete user
@router_user.delete("/users/{user_id}", status_code=204)
def eliminar_usuario(user_id: int):

    for i, u in enumerate(usuarios):

        if u.id == user_id:

            del usuarios[i]

            return

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
