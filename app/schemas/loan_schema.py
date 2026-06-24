from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")


class LoanUpdate(BaseModel):
    status: str = Field(..., description="Estado del préstamo: active, returned, overdue")


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {
        "from_attributes": True
    }


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = {
        "from_attributes": True
    }


class DeviceBasic(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {
        "from_attributes": True
    }


class LoanDetailResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str
    user: UserBasic
    device: DeviceBasic

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "loan_date": "2024-01-15T10:30:00",
                "return_date": None,
                "status": "active",
                "user": {
                    "id": 1,
                    "name": "Ana Pérez",
                    "email": "ana@sena.edu.co"
                },
                "device": {
                    "id": 3,
                    "name": "Laptop Lenovo ThinkPad",
                    "serial_number": "LEN-2024-001",
                    "device_type": "laptop"
                }
            }
        }
    }