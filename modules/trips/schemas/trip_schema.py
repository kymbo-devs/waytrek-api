from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TripBase(BaseModel):
    title: str


class TripCreate(TripBase):
    pass

class ActivityCreate(BaseModel):
    name: str = Field(..., description="The name of the activity")
    description: str = Field(..., description="The description of the activity")
    location_id: int = Field(..., description="The location of the activity")
    is_active: bool = Field(False, description="Whether the activity is active by default")
    history: str | None = Field(default=None, description="The history of the activity")
    tip: str | None = Field(default=None, description="The tip of the activity")
    movie: str | None = Field(default=None, description="The movie of the activity")
    clothes: str | None = Field(default=None, description="The clothes of the activity")
    tags: List[str] = Field(default=[], description="Tags to categorize the activity")


class ActivityUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    location_id: int | None = None
    is_active: bool | None = None
    history: str | None = None
    tip: str | None = None
    movie: str | None = None
    clothes: str | None = None
    tags: List[str] | None = None


class Activity(ActivityCreate):
    id: int

    class Config:
        from_attributes = True

class ActivityFilter(BaseModel):
    skip: int = 0
    limit: int = 100
    location_id: Optional[int] = None
    is_active: Optional[bool] = None
    tag: Optional[str] = Field(default=None, description="Search activities by partial tag match")


class VideoCreate(BaseModel):
    title: str = Field(..., description="The title of the video")
    description: str = Field(..., description="The description of the video")

class Video(VideoCreate):
    id: int

    class Config:
        from_attributes = True

class VideoSignedUrlResponse(BaseModel):
    video_id: int = Field(..., description="The ID of the video")
    signed_url: str = Field(..., description="The pre-signed URL to access the video")
    expires_in: int = Field(..., description="The expiration time in seconds")
