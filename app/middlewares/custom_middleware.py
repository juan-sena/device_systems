import time
import uuid
import logging

from fastapi import Request

# Configuración básica del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def custom_middleware(request: Request, call_next):
    """
    Middleware personalizado.
    Agrega información útil a cada respuesta.
    """

    start_time = time.time()

    request_id = str(uuid.uuid4())

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-App-Name"] = "device_systems API"
    response.headers["X-Request-ID"] = request_id

    # Registro de la petición
    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.4f}s "
        f"Request-ID={request_id}"
    )

    return response