from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func
from fastapi import HTTPException, status, UploadFile
from typing import List
from modules.activities.schemas.activity_schema import ActivityVideosFilters, ActivityVideosResponse
from modules.activities.schemas.activity_schema import ActivityCreate, ActivityUpdate, ActivityFilter, VideoUpdate, ActivityResponse
from modules.activities.models.activity import Activity, Location, ActivityVideos, ActivityPhotos, ActivityReviews, ActivityTips
from utils.s3_client import upload_file_to_s3, generate_presigned_url
from utils.error_models import ErrorCode, create_error_response
import uuid
import os

ALLOWED_VIDEO_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo"]

def transform_activity_to_response(activity: Activity) -> ActivityResponse:
    foodie_tips = []
    weather_and_clothing_tips = []
    pro_travelers_tips = []
    
    for tip in activity.tips:
        if tip.tip_type == "foodie":
            foodie_tips.append(tip.tip)
        elif tip.tip_type == "weather_clothing":
            weather_and_clothing_tips.append(tip.tip)
        elif tip.tip_type == "pro_traveler":
            pro_travelers_tips.append(tip.tip)
 
    reviews = [review.content for review in activity.reviews]
    
    return ActivityResponse(
        id=activity.id,
        name=activity.name,
        description=activity.description,
        location_id=activity.location_id,
        is_active=activity.is_active,
        history=activity.history,
        movie=activity.movie,
        clothes=activity.clothes,
        tags=activity.tags,
        population=activity.population,
        title=activity.title,
        category=activity.category,
        city=activity.city,
        country_code=activity.country_code,
        location_name=activity.location_name,
        weather=activity.weather,
        entrance=activity.entrance,
        opening_hours=activity.opening_hours,
        rating=activity.rating,
        foundation_date=activity.foundation_date,
        price_min=activity.price_min,
        price_max=activity.price_max,
        photos=activity.photos,
        reviews=reviews,
        foodie_tips=foodie_tips,
        weather_and_clothing_tips=weather_and_clothing_tips,
        pro_travelers_tips=pro_travelers_tips
    )

def create_activity(activity: ActivityCreate, db: Session):
    location = db.query(Location).filter(Location.id == activity.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.LOCATION_NOT_FOUND,
                f"Location with id {activity.location_id} not found."
            )
        )
    
    new_activity = Activity(
        name=activity.name,
        description=activity.description,
        location_id=activity.location_id,
        is_active=activity.is_active,
        history=activity.history,
        movie=activity.movie,
        clothes=activity.clothes,
        tags=activity.tags,
        population=activity.population,
        title=activity.title,
        category=activity.category,
        city=activity.city,
        country_code=activity.country_code,
        location_name=activity.location_name,
        weather=activity.weather,
        entrance=activity.entrance,
        opening_hours=activity.opening_hours,
        rating=activity.rating,
        foundation_date=activity.foundation_date,
        price_min=activity.price_min,
        price_max=activity.price_max
    )
    
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    

    for photo in activity.photos:
        if photo.url.strip():
            activity_photo = ActivityPhotos(
                activity_id=new_activity.id,
                name=photo.name,
                url=photo.url
            )
            db.add(activity_photo)
    
    for review_content in activity.reviews:
        if review_content.strip():
            activity_review = ActivityReviews(
                activity_id=new_activity.id,
                content=review_content
            )
            db.add(activity_review)
    
    # Crear tips relacionados
    # Tips de foodie
    for tip_content in activity.foodie_tips:
        if tip_content.strip():
            activity_tip = ActivityTips(
                activity_id=new_activity.id,
                tip_type="foodie",
                tip=tip_content
            )
            db.add(activity_tip)
    
    # Tips de weather_clothing
    for tip_content in activity.weather_and_clothing_tips:
        if tip_content.strip():
            activity_tip = ActivityTips(
                activity_id=new_activity.id,
                tip_type="weather_clothing",
                tip=tip_content
            )
            db.add(activity_tip)
    
    # Tips de pro_traveler
    for tip_content in activity.pro_travelers_tips:
        if tip_content.strip():
            activity_tip = ActivityTips(
                activity_id=new_activity.id,
                tip_type="pro_traveler",
                tip=tip_content
            )
            db.add(activity_tip)
    
    db.commit()
    db.refresh(new_activity)
    return new_activity

def get_activity_db(activity_id: int, db: Session) -> Activity:
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.ACTIVITY_NOT_FOUND,
                f"Activity with id {activity_id} not found."
            )
        )
    return activity

def get_activity(activity_id: int, db: Session) -> ActivityResponse:
    activity = db.query(Activity).options(
        selectinload(Activity.photos),
        selectinload(Activity.reviews),
        selectinload(Activity.tips)
    ).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.ACTIVITY_NOT_FOUND,
                f"Activity with id {activity_id} not found."
            )
        )
    
    return transform_activity_to_response(activity)

def get_activities(db: Session, filters: ActivityFilter) -> List[ActivityResponse]:
    query = db.query(Activity).options(
        selectinload(Activity.photos),
        selectinload(Activity.reviews),
        selectinload(Activity.tips)
    )
    
    if filters.location_id is not None:
        query = query.filter(Activity.location_id == filters.location_id)
        
    if filters.is_active is not None:
        query = query.filter(Activity.is_active == filters.is_active)
    
    if filters.tag is not None:
        query = query.filter(
            func.array_to_string(Activity.tags, ',').ilike(f"%{filters.tag}%")
        )
    
    if filters.min_price is not None:
        query = query.filter(Activity.price >= filters.min_price)
    
    if filters.max_price is not None:
        query = query.filter(Activity.price <= filters.max_price)
    
    if filters.min_population is not None:
        query = query.filter(Activity.population >= filters.min_population)
    
    if filters.max_population is not None:
        query = query.filter(Activity.population <= filters.max_population)
    
    # Nuevos filtros
    if filters.category is not None:
        query = query.filter(Activity.category.ilike(f"%{filters.category}%"))
    
    if filters.city is not None:
        query = query.filter(Activity.city.ilike(f"%{filters.city}%"))
    
    if filters.country_code is not None:
        query = query.filter(Activity.country_code == filters.country_code)
    
    if filters.min_rating is not None:
        query = query.filter(Activity.rating >= filters.min_rating)
    
    if filters.max_rating is not None:
        query = query.filter(Activity.rating <= filters.max_rating)
    
    query = query.order_by(Activity.population.desc())
        
    activities = query.offset(filters.skip).limit(filters.limit).all()
    
    # Transformar cada actividad al formato de respuesta
    return [transform_activity_to_response(activity) for activity in activities]

def update_activity(activity_id: int, activity_data: ActivityUpdate, db: Session):
    activity = get_activity_db(activity_id, db)
    
    update_data = activity_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(activity, key, value)
        
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def delete_activity(activity_id: int, db: Session):
    activity = get_activity_db(activity_id, db)
    
    db.delete(activity)
    db.commit()
    
    return {"detail": "Activity deleted successfully"}

def format_activity_video(video: ActivityVideos) -> ActivityVideosResponse:
    return {
        "activity_id": video.activity_id,
        "description": video.description,
        "file_key": video.file_key,
        "title": video.title,
        "video_id": video.id
    }  # type: ignore
    
def get_videos(db: Session, filters: ActivityVideosFilters = ActivityVideosFilters()):
    statement = select(ActivityVideos)
    if (filters.activity_id != None):
        statement = statement.where(ActivityVideos.activity_id == filters.activity_id)
    videos = list(db.execute(statement).scalars().all())
    return list(map(format_activity_video, videos))

def create_video(activity_id: int, video: UploadFile, title: str, description: str, db: Session):
    activity = get_activity_db(activity_id, db)
    
    if video.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                ErrorCode.INVALID_VIDEO_TYPE,
                f"Invalid video type. Allowed types are: {', '.join(ALLOWED_VIDEO_TYPES)}"
            )
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
            detail=create_error_response(
                ErrorCode.VIDEO_UPLOAD_ERROR,
                f"Error uploading video: {str(e)}"
            )
        )
    

def get_video_signed_url(activity_id: int, video_id: int, db: Session, expires_in: int = 3600):

    video = db.query(ActivityVideos).filter(
        ActivityVideos.id == video_id,
        ActivityVideos.activity_id == activity_id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.VIDEO_NOT_FOUND,
                f"Video with id {video_id} not found for activity {activity_id}."
            )
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
            detail=create_error_response(
                ErrorCode.SIGNED_URL_ERROR,
                f"Error generating signed URL: {str(e)}"
            )
        )

def delete_video(activity_id: int, video_id: int, db: Session):
    """Delete a video from both database and S3 storage."""
    activity = get_activity_db(activity_id, db)
    
    video = db.query(ActivityVideos).filter(
        ActivityVideos.id == video_id,
        ActivityVideos.activity_id == activity_id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.VIDEO_NOT_FOUND,
                f"Video with id {video_id} not found for activity {activity_id}."
            )
        )
    
    file_key = video.file_key
    
    try:
        from utils.s3_client import delete_file_from_s3
        delete_file_from_s3(file_key)
        
        db.delete(video)
        db.commit()
        
        return {"detail": f"Video {video_id} deleted successfully from activity {activity_id}"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                ErrorCode.VIDEO_DELETE_ERROR,
                f"Error deleting video: {str(e)}"
            )
        )

def update_video(activity_id: int, video_id: int, video_data: VideoUpdate, db: Session):
    """Update video title and/or description in the database."""
    activity = get_activity_db(activity_id, db)
    
    video = db.query(ActivityVideos).filter(
        ActivityVideos.id == video_id,
        ActivityVideos.activity_id == activity_id
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.VIDEO_NOT_FOUND,
                f"Video with id {video_id} not found for activity {activity_id}."
            )
        )
    
    update_data = video_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(
                ErrorCode.VALIDATION_ERROR,
                "At least one field (title or description) must be provided for update."
            )
        )
    
    for key, value in update_data.items():
        setattr(video, key, value)
    
    try:
        db.add(video)
        db.commit()
        db.refresh(video)
        
        return video
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(
                ErrorCode.INTERNAL_SERVER_ERROR,
                f"Error updating video: {str(e)}"
            )
        )
