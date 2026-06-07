from fastapi import HTTPException
from app.data.users_db import usuarios


def get_user_or_404(user_id: int):

    for usuario in usuarios:

        if usuario.id == user_id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )