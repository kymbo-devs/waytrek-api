from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, ARRAY, Text
from sqlalchemy.orm import relationship, Mapped
from db.session import Base
from modules.users.models.user import User


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="cascade"))

    location: Mapped['Location'] = relationship(back_populates="trips")
    user: Mapped['User'] = relationship(back_populates="trips")
    documents: Mapped[List['TripDocuments']] = relationship(back_populates="trip")
    trip_schedule: Mapped[List['TripSchedule']] = relationship(back_populates="trip")
    

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String)
    nickname = Column(String)
    flag_url = Column(String)

    activities: Mapped[List['Activity']] = relationship(back_populates="location")
    trips: Mapped[List['Trip']] = relationship(back_populates="location")


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


class TripDocuments(Base):
    __tablename__ = "trip_documents"
    
    id = Column(Integer, primary_key=True, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="cascade"))
    url = Column(String, nullable=False)
    type = Column(String, nullable=False)
    file_key = Column(String, nullable=False)

    trip: Mapped['Trip'] = relationship(back_populates="documents")

class TripSchedule(Base):
    __tablename__ = "trip_schedule"
    
    id = Column(Integer, primary_key=True, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="cascade"))
    date = Column(DateTime, nullable=False)

    trip: Mapped['Trip'] = relationship(back_populates="trip_schedule")
    schedule: Mapped[List['Schedule']] = relationship(back_populates="trip_schedule")

class Schedule(Base):
    __tablename__ = "schedule"
    
    id = Column(Integer, primary_key=True, nullable=False)
    trip_schedule_id = Column(Integer, ForeignKey("trip_schedule.id", ondelete="cascade"))
    hour = Column(String, nullable=False)
    activity_name = Column(String, nullable=False)

    trip_schedule: Mapped['TripSchedule'] = relationship(back_populates="schedule")

User.trips = relationship('Trip', back_populates="user")