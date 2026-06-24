from fastapi import FastAPI

from app.routes.user_routes import router_user
from app.routes.device_routes import router_device
from app.routes.loan_routes import router_loan

from app.database.connection import engine, Base
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios, dispositivos y préstamos del sistema device_systems",
    version="3.0.0",
    contact={
        "name": "Juan Noriega",
        "email": "juannoriegasena@gmail.com"
    }
)

app.include_router(router_user)
app.include_router(router_device)
app.include_router(router_loan)
