from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
from modules.trips.schemas.trip_schema import TripCreate

def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    return trip

def get_trip(trip_id: int, db: Session = Depends(get_db)):
    return {
        "id": 1,
        "title": "Test",
        "content": "Test"
    }