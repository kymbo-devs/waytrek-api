from typing import List
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, ARRAY, Text, DECIMAL, Float
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
    title = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    country_code = Column(Text, nullable=True)
    location_name = Column(Text, nullable=True)
    weather = Column(Text, nullable=True)
    entrance = Column(Text, nullable=True)
    opening_hours = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    foundation_date = Column(Text, nullable=True)
    price_min = Column(Integer, nullable=True)
    price_max = Column(Integer, nullable=True)
    history = Column(String, nullable=False)
    movie = Column(String, nullable=False)
    clothes = Column(String, nullable=False)
    tags = Column(ARRAY(Text), default=lambda: [], nullable=False)
    population = Column(Integer, nullable=True)

    location: Mapped['Location'] = relationship(back_populates="activities")
    videos: Mapped[List['ActivityVideos']] = relationship(back_populates="activity")
    photos: Mapped[List['ActivityPhotos']] = relationship(back_populates="activity")
    reviews: Mapped[List['ActivityReviews']] = relationship(back_populates="activity")
    tips: Mapped[List['ActivityTips']] = relationship(back_populates="activity")

class ActivityVideos(Base):
    __tablename__ = "activity_videos"
    
    id = Column(Integer, primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="cascade"))
    url = Column(String, nullable=False)
    file_key = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    activity: Mapped['Activity'] = relationship(back_populates="videos")

class ActivityPhotos(Base):
    __tablename__ = "activity_photos"
    
    id = Column(Integer, primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="cascade"), nullable=False)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    activity: Mapped['Activity'] = relationship(back_populates="photos")

class ActivityReviews(Base):
    __tablename__ = "activity_reviews"
    
    id = Column(Integer, primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="cascade"), nullable=False)
    content = Column(Text, nullable=False)

    activity: Mapped['Activity'] = relationship(back_populates="reviews")

class ActivityTips(Base):
    __tablename__ = "activity_tips"
    
    id = Column(Integer, primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="cascade"), nullable=False)
    tip_type = Column(Text, nullable=False)  # 'foodie', 'weather_clothing', 'pro_traveler'
    tip = Column(Text, nullable=False)

    activity: Mapped['Activity'] = relationship(back_populates="tips")

Location.activities = relationship(Activity, back_populates="location")