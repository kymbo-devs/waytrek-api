from typing import List
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, ARRAY, Text, DECIMAL
from sqlalchemy.orm import relationship, Mapped
from db.session import Base
from modules.locations.models.location import Location

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="cascade"))
    is_active = Column(Boolean, default=False)
    history = Column(String, nullable=False)
    tip = Column(String, nullable=False)
    movie = Column(String, nullable=False)
    clothes = Column(String, nullable=False)
    tags = Column(ARRAY(Text), default=lambda: [], nullable=False)
    price = Column(DECIMAL(10, 2), nullable=True)
    photo_url = Column(String, nullable=True)
    population = Column(Integer, nullable=True)

    location: Mapped['Location'] = relationship(back_populates="activities")
    videos: Mapped[List['ActivityVideos']] = relationship(back_populates="activity")

class ActivityVideos(Base):
    __tablename__ = "activity_videos"
    
    id = Column(Integer, primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="cascade"))
    url = Column(String, nullable=False)
    file_key = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    activity: Mapped['Activity'] = relationship(back_populates="videos")


Location.activities = relationship(Activity, back_populates="location")