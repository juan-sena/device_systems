from fastapi import APIRouter, Response
from app.schemas.user_schema import Usuario, UsuarioResponse

router_user = APIRouter()

usuarios = []


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
def obtener_usuario_por_id(user_id: int):

    for usuario in usuarios:
        if usuario.id == user_id:
            return usuario

    return {"mensaje": "Usuario no encontrado"}


# POST users
@router_user.post("/users", response_model=UsuarioResponse)
def crear_usuario(
    usuario: Usuario,
    response: Response
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for u in usuarios:
        if u.email == usuario.email:
            return {
                "mensaje": "El correo ya existe"
            }

    usuarios.append(usuario)

    return usuario