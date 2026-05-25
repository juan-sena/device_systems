from fastapi import FastAPI
from app.routes.user_routes import router_user

app = FastAPI()

app.include_router(router_user)