from typing import List
from sqlalchemy.orm import Session
from modules.trips.schemas.activity_schema import ActivityVideosFilters, ActivityVideosResponse
from modules.trips.models.trip import ActivityVideos
from modules.trips.services import activities_service


def get_activity_videos(activity_id: int, db: Session) -> List[ActivityVideosResponse]:
    def format_activity_video(video: ActivityVideos) -> ActivityVideosResponse:
        return {
            "activity_id": video.activity_id,
            "description": video.description,
            "file_key": video.file_key,
            "title": video.title,
            "video_id": video.id
        }  # type: ignore
    videos = activities_service.get_videos(db, ActivityVideosFilters(activity_id=activity_id))
    return list(map(format_activity_video, videos))
