from typing import List
from fastapi import APIRouter, Depends
from modules.trips.controllers import activity_controller
from db.session import get_db
from modules.trips.schemas.activity_schema import ActivityVideosResponse
from routes import HttpErrorResponse

router = APIRouter()


@router.get('/{activity_id}/videos', responses={
    "404": {"model": HttpErrorResponse, "description": "Activity not found"},
},
    summary="Get videos associated to an activity",
    description="Get videos from an activity. Returns 404 if there's not activity with the provided id",)
def get_activity_videos(activity_id: int, db=Depends(get_db)) -> List[ActivityVideosResponse]:
    return activity_controller.get_activity_videos(activity_id=activity_id, db=db)
