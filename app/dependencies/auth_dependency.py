from fastapi import Depends, HTTPException, status

from app.auth.security import get_current_user
from app.models.user_model import User


def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    """
    Verifica que el usuario esté activo.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo."
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
):
    """
    Permite únicamente usuarios con rol admin.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos."
        )

    return current_user


def require_admin_or_support(
    current_user: User = Depends(get_current_active_user)
):
    """
    Permite usuarios con rol admin o support.
    """

    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos."
        )

    return current_user