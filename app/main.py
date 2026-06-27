from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.config.limiter import limiter

from app.middlewares.custom_middleware import custom_middleware

from app.routes.user_routes import router_user
from app.routes.device_routes import router_device
from app.routes.loan_routes import router_loan
from app.auth.auth_routes import router_auth

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

# ==========================
# Rate Limiting
# ==========================

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)

# ==========================
# Configuración de CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware personalizado


app.middleware("http")(custom_middleware)

app.include_router(router_user)
app.include_router(router_device)
app.include_router(router_loan)
app.include_router(router_auth)