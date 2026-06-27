from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.config.limiter import limiter

from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin_or_support
)
from app.models.user_model import User

from app.schemas.loan_schema import (
    LoanCreate,
    LoanUpdate,
    LoanResponse,
    LoanDetailResponse
)
from app.dependencies.database_dependency import get_db
from app.services.loan_service import (
    create_loan,
    get_loans,
    get_loan_by_id,
    return_loan,
    get_loans_with_details,
    get_loans_by_user,
    get_loans_by_device,
    get_loans_filtered
)
from app.services.user_service import get_user_by_id
from app.services.device_service import get_device_by_id

router_loan = APIRouter(tags=["Loans"])


@router_loan.get(
    "/loans/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con detalles",
    description="Obtiene todos los préstamos registrados con información del usuario y del dispositivo."
)
def obtener_prestamos_detalles(
    db: Session = Depends(get_db)
):
    return get_loans_with_details(db)


@router_loan.get(
    "/loans",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con filtros",
    description="Obtiene préstamos registrados. Permite filtrar por estado, correo de usuario o tipo de dispositivo."
)
def obtener_prestamos(
    status: str = Query(None, description="Filtrar por estado: active, returned, overdue"),
    user_email: str = Query(None, description="Filtrar por correo del usuario"),
    device_type: str = Query(None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db)
):
    if any([status, user_email, device_type]):
        return get_loans_filtered(db, status, user_email, device_type)
    return get_loans_with_details(db)


@router_loan.get(
    "/loans/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Obtener préstamo por ID",
    description="Obtiene los detalles de un préstamo específico, incluyendo información del usuario y dispositivo.",
    responses={
        200: {"description": "Préstamo encontrado exitosamente"},
        404: {"description": "Préstamo no encontrado"}
    }
)
def obtener_prestamo_por_id(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


@router_loan.post(
    "/loans",
    response_model=LoanDetailResponse,
    status_code=201,
    summary="Crear préstamo",
    description="Registra un nuevo préstamo. Valida que el usuario y el dispositivo existan, y que el dispositivo esté disponible.",
    responses={
        201: {"description": "Préstamo creado exitosamente"},
        404: {"description": "Usuario o dispositivo no encontrado"},
        409: {"description": "Dispositivo no disponible"}
    }
)
@limiter.limit("10/minute")
def crear_prestamo(
    request: Request,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    user = get_user_by_id(db, loan_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = get_device_by_id(db, loan_data.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail="El dispositivo no está disponible para préstamo"
        )

    return create_loan(db, loan_data)


@router_loan.patch(
    "/loans/{loan_id}/return",
    response_model=LoanDetailResponse,
    summary="Devolver dispositivo",
    description="Registra la devolución de un dispositivo. Marca el préstamo como 'returned', asigna fecha de devolución y cambia la disponibilidad del dispositivo.",
    responses={
        200: {"description": "Devolución registrada exitosamente"},
        404: {"description": "Préstamo no encontrado"},
        409: {"description": "El préstamo ya fue devuelto"}
    }
)
def devolver_prestamo(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")

    return return_loan(db, loan)


@router_loan.get(
    "/users/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Préstamos de un usuario",
    description="Obtiene todos los préstamos asociados a un usuario específico.",
    responses={
        200: {"description": "Lista de préstamos del usuario"},
        404: {"description": "Usuario no encontrado"}
    }
)
def obtener_prestamos_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return get_loans_by_user(db, user_id)


@router_loan.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Obtiene el historial completo de préstamos de un dispositivo específico.",
    responses={
        200: {"description": "Historial de préstamos del dispositivo"},
        404: {"description": "Dispositivo no encontrado"}
    }
)
def obtener_prestamos_dispositivo(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return get_loans_by_device(db, device_id)