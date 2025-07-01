from typing import Optional
from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    country: str = Field(..., description="The country name")
    city: str = Field(..., description="The city name")
    nickname: Optional[str] = Field(None, description="A nickname for the location")
    flag_url: Optional[str] = Field(None, description="URL to the country flag image")


class LocationUpdate(BaseModel):
    country: Optional[str] = Field(None, description="The country name")
    city: Optional[str] = Field(None, description="The city name")
    nickname: Optional[str] = Field(None, description="A nickname for the location")
    flag_url: Optional[str] = Field(None, description="URL to the country flag image")


class Location(LocationCreate):
    id: int

    class Config:
        from_attributes = True


class LocationFilter(BaseModel):
    skip: int = Field(0, description="Number of records to skip for pagination")
    limit: int = Field(100, description="Maximum number of records to return")
    country: Optional[str] = Field(None, description="Filter by country name (partial match)")
    city: Optional[str] = Field(None, description="Filter by city name (partial match)") 