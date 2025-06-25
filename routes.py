from fastapi import APIRouter
from utils.error_models import (
    ValidationErrorResponse, 
    ServerErrorResponse,
    AuthTokenErrorResponse
)
from modules.users.routes.user_routes import router as users_router
from modules.trips.routes.trip_routes import router as trips_router
from modules.tips.routes.tip_routes import router as tips_router
from config import settings

router = APIRouter(prefix=settings.API_PREFIX, responses={
     401: { "model": AuthTokenErrorResponse, "description": "Unauthorized - Invalid or missing token" },
     422: { "model": ValidationErrorResponse, "description": "Validation Error - Invalid input data" },
     500: { "model": ServerErrorResponse, "description": "Internal Server Error" }
})

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(trips_router, prefix="/trips", tags=["trips"])
router.include_router(tips_router, prefix="/tips", tags=["tips"])







