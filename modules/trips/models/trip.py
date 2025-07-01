from typing import List
from sqlalchemy import  Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, Mapped
from db.session import Base
from modules.activities.models.location import Location
from modules.users.models.user import User



class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="cascade"))

    location: Mapped['Location'] = relationship(back_populates="trips")
    documents: Mapped[List['TripDocuments']] = relationship(back_populates="trip")
    trip_schedule: Mapped[List['TripSchedule']] = relationship(back_populates="trip")
    
User.trips = relationship(Trip, back_populates="user")
Trip.user= relationship(User, back_populates="trips")
Location.trips = relationship(Trip, back_populates="location")

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