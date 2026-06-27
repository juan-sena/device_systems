from slowapi import Limiter
from slowapi.util import get_remote_address

# Crea el limitador utilizando la IP del cliente
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"]
)