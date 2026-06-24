from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, description="Nombre del dispositivo")
    serial_number: str = Field(..., min_length=1, description="Número de serie único")
    device_type: str = Field(..., description="Tipo de dispositivo: laptop, tablet, proyector, cámara, router, monitor")
    brand: Optional[str] = Field(default=None, description="Marca del dispositivo")


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=2)
    serial_number: str = Field(..., min_length=1)
    device_type: str = Field(...)
    brand: Optional[str] = None


class DevicePatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2)
    serial_number: Optional[str] = Field(default=None, min_length=1)
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True,
                "created_at": "2024-01-15T10:30:00"
            }
        }
    }