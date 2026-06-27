from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    require_admin,
    require_admin_or_support
)
from app.models.user_model import User

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch,
    DeviceResponse
)
from app.dependencies.database_dependency import get_db
from app.services.device_service import (
    create_device,
    get_devices,
    get_device_by_id,
    get_device_by_serial,
    update_device,
    patch_device,
    delete_device,
    get_devices_filtered
)

router_device = APIRouter(tags=["Devices"])


@router_device.get(
    "/devices",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos registrados. Permite filtrar por tipo, disponibilidad, marca o búsqueda general."
)
def obtener_dispositivos(
    device_type: str = Query(None, description="Filtrar por tipo de dispositivo (laptop, tablet, proyector, etc.)"),
    is_available: bool = Query(None, description="Filtrar por disponibilidad"),
    brand: str = Query(None, description="Filtrar por marca"),
    search: str = Query(None, description="Búsqueda general por nombre, serial o marca"),
    db: Session = Depends(get_db)
):
    if any([device_type, is_available is not None, brand, search]):
        return get_devices_filtered(db, device_type, is_available, brand, search)
    return get_devices(db)


@router_device.get(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
    description="Obtiene los detalles de un dispositivo específico mediante su ID.",
    responses={
        200: {"description": "Dispositivo encontrado exitosamente"},
        404: {"description": "Dispositivo no encontrado"}
    }
)
def obtener_dispositivo_por_id(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router_device.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo tecnológico en el sistema.",
    responses={
        201: {"description": "Dispositivo creado exitosamente"},
        400: {"description": "Número de serie duplicado"},
        422: {"description": "Error de validación de datos"}
    }
)
def crear_dispositivo(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    existing = get_device_by_serial(db, device_data.serial_number)
    if existing:
        raise HTTPException(status_code=400, detail="El número de serie ya existe")
    return create_device(db, device_data)


@router_device.put(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente los datos de un dispositivo existente.",
    responses={
        200: {"description": "Dispositivo actualizado exitosamente"},
        404: {"description": "Dispositivo no encontrado"},
        400: {"description": "Número de serie duplicado"}
    }
)
def actualizar_dispositivo(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support)
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    existing = get_device_by_serial(db, device_data.serial_number)
    if existing and existing.id != device_id:
        raise HTTPException(status_code=400, detail="El número de serie ya existe")

    return update_device(db, device, device_data)


@router_device.patch(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    description="Actualiza parcialmente los datos de un dispositivo existente.",
    responses={
        200: {"description": "Dispositivo actualizado exitosamente"},
        404: {"description": "Dispositivo no encontrado"},
        400: {"description": "Debe enviar al menos un campo para actualizar"}
    }
)
def actualizar_dispositivo_parcial(
    device_id: int,
    device_data: DevicePatch,
    db: Session = Depends(get_db)
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    data = device_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo para actualizar")

    if "serial_number" in data:
        existing = get_device_by_serial(db, data["serial_number"])
        if existing and existing.id != device_id:
            raise HTTPException(status_code=400, detail="El número de serie ya existe")

    return patch_device(db, device, data)


@router_device.delete(
    "/devices/{device_id}",
    status_code=204,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema.",
    responses={
        204: {"description": "Dispositivo eliminado exitosamente"},
        404: {"description": "Dispositivo no encontrado"}
    }
)
def eliminar_dispositivo(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    delete_device(db, device)
    return