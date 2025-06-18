from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile, File, Form

from modules.trips.controllers import activity_controller
from modules.trips.schemas.activity_schema import ActivityVideosResponse
from modules.trips.schemas.trip_schema import Activity, ActivityCreate, ActivityUpdate, ActivityFilter, VideoSignedUrlResponse
from modules.trips.controllers.trip_controller import (
    create_trip as create_trip_controller, 
    get_trip as get_trip_controller,
    create_activity_controller,
    get_activities_controller,
    get_activity_controller,
    update_activity_controller,
    delete_activity_controller,
    create_video_controller,
    get_video_signed_url_controller
)
from db.session import get_db

router = APIRouter()

@router.post(
    "/activities",
    response_model=Activity,
    status_code=201,
    summary="Create a new activity",
    description="Creates a new activity associated with a location, including details like history, tips, and media links.",
)
async def create_activity_route(activity: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity_controller(activity, db=db)

@router.get(
    "/activities",
    response_model=List[Activity],
    summary="List all activities",
    description="Retrieves a list of activities with optional filtering by location and active status, and supports pagination.",
)
async def get_activities_route(
    filters: ActivityFilter = Depends(),
    db: Session = Depends(get_db),
):
    return get_activities_controller(filters=filters, db=db)

@router.get(
    "/activities/{activity_id}",
    response_model=Activity,
    summary="Get a specific activity",
    description="Retrieves detailed information about a single activity by its ID.",
)
async def get_activity_route(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_controller(activity_id, db)

@router.patch(
    "/activities/{activity_id}",
    response_model=Activity,
    summary="Update an activity",
    description="Updates the data of an existing activity. All fields are optional.",
)
async def update_activity_route(
    activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)
):
    return update_activity_controller(activity_id, activity, db)

@router.delete(
    "/activities/{activity_id}",
    status_code=204,
    summary="Delete an activity",
    description="Deletes an activity from the system by its ID.",
)
async def delete_activity_route(activity_id: int, db: Session = Depends(get_db)):
    delete_activity_controller(activity_id, db)
    return

@router.post(
    "/activities/{activity_id}/videos",
    status_code=201,
    summary="Upload a video for an activity",
    description="""
    Uploads a video file for a specific activity.
    
    - The video must be in MP4, QuickTime, or AVI format
    - The file will be stored in S3 and made publicly accessible
    - A record will be created in the database with the video metadata
    
    Required fields:
    - video: The video file (multipart/form-data)
    - title: Title of the video
    - description: Description of the video
    """,
)
async def create_video_route(
    activity_id: int,
    video: UploadFile = File(..., description="The video file to upload"),
    title: str = Form(..., description="Title of the video"),
    description: str = Form(..., description="Description of the video"),
    db: Session = Depends(get_db)
):
    if not video:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video file is required"
        )
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )
    if not description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description is required"
        )
        
    return create_video_controller(activity_id, video, title, description, db)

@router.get('/activities/{activity_id}/videos',
    summary="Get videos associated to an activity",
    description="Get videos from an activity")
def get_activity_videos(activity_id: int, db=Depends(get_db)) -> List[ActivityVideosResponse]:
    return activity_controller.get_activity_videos(activity_id=activity_id, db=db)

@router.get(
    "/activities/{activity_id}/videos/{video_id}/url",
    response_model=VideoSignedUrlResponse,
    summary="Get a signed URL for a video",
    description="""
    Generates a temporary signed URL to access a video stored in S3.
    
    - Validates that the video belongs to the specified activity
    - Returns a URL that expires after 10 minutes (600 seconds)
    - Enables secure video playback directly in the browser
    - The signed URL prevents unauthorized access to video content
    """,
)
async def get_video_signed_url_route(activity_id: int, video_id: int, db: Session = Depends(get_db)):
    return get_video_signed_url_controller(activity_id, video_id, db)

