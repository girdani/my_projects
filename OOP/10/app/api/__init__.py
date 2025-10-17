from .client_api import router as client_router
from .service_api import router as service_router
from .appointment_api import router as appointment_router
from .administrator_api import router as administrator_router
from .user_api import router as user_router
from .dependency import get_session


__all__ = [
    "client_router",
    "service_router",
    "appointment_router",
    "administrator_router",
    "user_router",
    "get_session",
]