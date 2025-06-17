from typing import Any, NotRequired, Sequence
from typing_extensions import TypedDict
from fastapi import APIRouter
from error_handlers import HttpErrorResponse
from modules.users.routes.user_routes import router as users_router
from modules.trips.routes.trip_routes import router as trips_router
from modules.trips.routes.acitivity_routes import router as activities_routes
from modules.tips.routes.tip_routes import router as tips_router
from config import settings

router = APIRouter(prefix=settings.API_PREFIX, responses={
     422: { "model": HttpErrorResponse }
})

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(trips_router, prefix="/trips", tags=["trips"])
router.include_router(activities_routes, prefix="/activities", tags=["activities"])
router.include_router(tips_router, prefix="/tips", tags=["tips"])







