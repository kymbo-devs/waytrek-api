from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
from modules.trips.schemas.trip_schema import TripCreate, ActivityCreate, ActivityUpdate, ActivityFilter
from modules.trips.services import activities_service

def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    return trip

def get_trip(trip_id: int, db: Session = Depends(get_db)):
    return {
        "id": 1,
        "title": "Test",
        "content": "Test"
    }


def create_activity_controller(activity: ActivityCreate, db: Session):
    return activities_service.create_activity(activity, db)
     
def get_activities_controller(filters: ActivityFilter, db: Session):
    return activities_service.get_activities(db=db, filters=filters)

def get_activity_controller(activity_id: int, db: Session):
    return activities_service.get_activity(activity_id=activity_id, db=db)

def update_activity_controller(activity_id: int, activity_data: ActivityUpdate, db: Session):
    return activities_service.update_activity(activity_id=activity_id, activity_data=activity_data, db=db)

def delete_activity_controller(activity_id: int, db: Session):
    return activities_service.delete_activity(activity_id=activity_id, db=db)
     
