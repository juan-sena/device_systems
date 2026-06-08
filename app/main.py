from fastapi import FastAPI

from app.routes.user_routes import router_user

from app.database.connection import engine, Base
from app.models.user_model import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems",
    version="2.0.0",
    contact={
        "name": "Juan Noriega",
        "email": "juannoriegasena@gmail.com"
    }
)

app.include_router(router_user)