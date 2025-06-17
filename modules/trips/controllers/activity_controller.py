from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.trips.schemas.activity_schema import ActivityVideosResponse
from modules.trips.models.trip import Activity, ActivityVideos


def get_activity_videos(activity_id: int, db: Session) -> List[ActivityVideosResponse]:
    activity = db.execute(select(Activity).where(
        Activity.id == activity_id)).scalar_one_or_none()
    if (not activity):
        raise HTTPException(404, "Activity not found")

    def format_activity_video(video: ActivityVideos) -> ActivityVideosResponse:
        return {
            "activity_id": video.activity_id,
            "description": video.description,
            "file_key": video.file_key,
            "title": video.title,
            "video_id": video.id
        }  # type: ignore

    return list(map(format_activity_video, activity.videos))
