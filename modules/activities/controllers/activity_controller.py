from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from modules.activities.schemas.activity_schema import ActivityCreate, ActivityFilter, ActivityUpdate, ActivityVideosFilters, ActivityVideosResponse, VideoUpdate, ActivityResponse
from modules.activities.services import activities_service


def get_activity_videos(activity_id: int, db: Session) -> List[ActivityVideosResponse]:
    return activities_service.get_videos(db, ActivityVideosFilters(activity_id=activity_id))


def create_activity_controller(activity: ActivityCreate, db: Session):
    return activities_service.create_activity(activity, db)


def get_activities_controller(filters: ActivityFilter, db: Session) -> List[ActivityResponse]:
    return activities_service.get_activities(db=db, filters=filters)


def get_activity_controller(activity_id: int, db: Session) -> ActivityResponse:
    return activities_service.get_activity(activity_id=activity_id, db=db)


def update_activity_controller(activity_id: int, activity_data: ActivityUpdate, db: Session):
    return activities_service.update_activity(activity_id=activity_id, activity_data=activity_data, db=db)


def delete_activity_controller(activity_id: int, db: Session):
    return activities_service.delete_activity(activity_id=activity_id, db=db)


def create_video_controller(activity_id: int, video: UploadFile, title: str, description: str, db: Session):
    return activities_service.create_video(activity_id=activity_id, video=video, title=title, description=description, db=db)


def get_video_signed_url_controller(activity_id: int, video_id: int, db: Session):
    return activities_service.get_video_signed_url(activity_id=activity_id, video_id=video_id, db=db)


def delete_video_controller(activity_id: int, video_id: int, db: Session):
    return activities_service.delete_video(activity_id=activity_id, video_id=video_id, db=db)


def update_video_controller(activity_id: int, video_id: int, video_data: VideoUpdate, db: Session):
    return activities_service.update_video(activity_id=activity_id, video_id=video_id, video_data=video_data, db=db)
