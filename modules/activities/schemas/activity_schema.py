from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class ActivityVideosResponse(TypedDict):
    video_id: int
    title: str
    description: str
    activity_id: int
    file_key: str

class ActivityVideosFilters(BaseModel):
    activity_id: Optional[int] = None

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
    price: float | None = Field(default=None, description="The price of the activity in USD", ge=0)
    photo_url: str | None = Field(default=None, description="URL of the activity photo")
    population: int | None = Field(default=None, description="Population of the area where the activity takes place", ge=0)


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
    price: float | None = Field(default=None, description="The price of the activity in USD", ge=0)
    photo_url: str | None = Field(default=None, description="URL of the activity photo")
    population: int | None = Field(default=None, description="Population of the area where the activity takes place", ge=0)


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
    min_price: Optional[float] = Field(default=None, description="Minimum price filter", ge=0)
    max_price: Optional[float] = Field(default=None, description="Maximum price filter", ge=0)
    min_population: Optional[int] = Field(default=None, description="Minimum population filter", ge=0)
    max_population: Optional[int] = Field(default=None, description="Maximum population filter", ge=0)


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

class VideoUpdate(BaseModel):
    title: str | None = Field(default=None, description="The title of the video")
    description: str | None = Field(default=None, description="The description of the video")
