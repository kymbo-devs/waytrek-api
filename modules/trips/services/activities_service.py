from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from modules.trips.schemas.trip_schema import ActivityCreate, ActivityUpdate, ActivityFilter
from modules.trips.models.trip import Activity, Location, ActivityVideos
from utils.s3_client import upload_file_to_s3, generate_presigned_url
import uuid
import os

ALLOWED_VIDEO_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo"]

def create_activity(activity: ActivityCreate, db: Session):
    location = db.query(Location).filter(Location.id == activity.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {activity.location_id} not found."
        )
    
    new_activity = Activity(
        name=activity.name,
        description=activity.description,
        location_id=activity.location_id,
        is_active=activity.is_active,
        history=activity.history,
        tip=activity.tip,
        movie=activity.movie,
        clothes=activity.clothes
        )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

def get_activity(activity_id: int, db: Session):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )
    return activity

def get_activities(db: Session, filters: ActivityFilter):
    query = db.query(Activity)
    
    if filters.location_id is not None:
        query = query.filter(Activity.location_id == filters.location_id)
        
    if filters.is_active is not None:
        query = query.filter(Activity.is_active == filters.is_active)
        
    activities = query.offset(filters.skip).limit(filters.limit).all()
    return activities

def update_activity(activity_id: int, activity_data: ActivityUpdate, db: Session):
    activity = get_activity(activity_id, db)
    
    update_data = activity_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(activity, key, value)
        
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def delete_activity(activity_id: int, db: Session):
    activity = get_activity(activity_id, db)
    
    db.delete(activity)
    db.commit()
    
    return {"detail": "Activity deleted successfully"}

def create_video(activity_id: int, video: UploadFile, title: str, description: str, db: Session):
    activity = get_activity(activity_id, db)
    
    if video.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid video type. Allowed types are: {', '.join(ALLOWED_VIDEO_TYPES)}"
        )
    
    file_extension = os.path.splitext(video.filename)[1]
    file_key = f"activities/{activity_id}/{uuid.uuid4()}{file_extension}"
    
    try:
        video_url = upload_file_to_s3(
            file_data=video.file,
            file_name=file_key,
            content_type=video.content_type
        )
        
        new_video = ActivityVideos(
            activity_id=activity_id,
            url=video_url,
            file_key=file_key,
            title=title,
            description=description
        )
        
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        
        return new_video
        
    except Exception as e:
        try:
            from utils.s3_client import delete_file_from_s3
            delete_file_from_s3(file_key)
        except:
            pass
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading video: {str(e)}"
        )
    

def get_video_signed_url(activity_id: int, video_id: int, db: Session, expires_in: int = 3600):

    video = db.query(ActivityVideos).filter(
        ActivityVideos.id == video_id,
        ActivityVideos.activity_id == activity_id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found for activity {activity_id}."
        )
    
    try:
        signed_url = generate_presigned_url(video.file_key, expires_in)
        
        return {
            "video_id": video_id,
            "signed_url": signed_url,
            "expires_in": expires_in
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating signed URL: {str(e)}"
        )
