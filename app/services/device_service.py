from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.device_model import Device


def create_device(db: Session, device_data):
    device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def get_devices(db: Session):
    return db.query(Device).all()


def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()


def get_device_by_serial(db: Session, serial: str):
    return db.query(Device).filter(Device.serial_number == serial).first()


def update_device(db: Session, device: Device, device_data):
    device.name = device_data.name
    device.serial_number = device_data.serial_number
    device.device_type = device_data.device_type
    device.brand = device_data.brand
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device: Device, data: dict):
    for field, value in data.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device):
    db.delete(device)
    db.commit()


def get_devices_filtered(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None
):
    query = db.query(Device)

    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%")
            )
        )

    return query.all()