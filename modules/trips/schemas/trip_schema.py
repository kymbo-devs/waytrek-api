from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TripBase(BaseModel):
    title: str


class TripCreate(TripBase):
    pass