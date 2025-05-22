from pydantic import BaseModel
from datetime import datetime


class TripBase(BaseModel):
    title: str


class TripCreate(TripBase):
    pass
