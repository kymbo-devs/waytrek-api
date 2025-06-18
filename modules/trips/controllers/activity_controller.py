from typing import List
from sqlalchemy.orm import Session
from modules.trips.schemas.activity_schema import ActivityVideosFilters, ActivityVideosResponse
from modules.trips.services import activities_service


def get_activity_videos(activity_id: int, db: Session) -> List[ActivityVideosResponse]:
    return activities_service.get_videos(db, ActivityVideosFilters(activity_id=activity_id))
