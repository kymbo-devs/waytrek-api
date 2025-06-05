from typing import List
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped
from db.session import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"))
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="cascade"))

    location: Mapped['Location'] = relationship(back_populates="trips")
    user = relationship("User", back_populates="trips")
    

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
    is_active = Column(Boolean, default=True)

    location: Mapped['Location'] = relationship(back_populates="trips")