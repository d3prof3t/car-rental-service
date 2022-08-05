from fastapi.routing import APIRouter

from car_rental_service.web.api import (
    docs,
    search,
    monitoring,
    reservation,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(
    reservation.router,
    prefix="/reservations",
    tags=["reservation"],
)
api_router.include_router(search.router, prefix="/search", tags=["search"])
