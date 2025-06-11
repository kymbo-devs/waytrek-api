from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.trips.schemas.trip_schema import ActivityCreate, ActivityUpdate, ActivityFilter
from modules.trips.models.trip import Activity, Location



def create_activity(activity: ActivityCreate, db: Session):
    
    location = db.query(Location).filter(Location.id == activity.location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {activity.location_id} not found."
        )
    
    new_activity = Activity(
        name=activity.name,
        description=activity.description,
        location_id=activity.location_id,
        is_active=activity.is_active,
        history=activity.history,
        tip=activity.tip,
        movie=activity.movie,
        clothes=activity.clothes
        )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

def get_activity(activity_id: int, db: Session):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found."
        )
    return activity

def get_activities(db: Session, filters: ActivityFilter):
    query = db.query(Activity)
    
    if filters.location_id is not None:
        query = query.filter(Activity.location_id == filters.location_id)
        
    if filters.is_active is not None:
        query = query.filter(Activity.is_active == filters.is_active)
        
    activities = query.offset(filters.skip).limit(filters.limit).all()
    return activities

def update_activity(activity_id: int, activity_data: ActivityUpdate, db: Session):
    activity = get_activity(activity_id, db)
    
    update_data = activity_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(activity, key, value)
        
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def delete_activity(activity_id: int, db: Session):
    activity = get_activity(activity_id, db)
    
    db.delete(activity)
    db.commit()
    
    return {"detail": "Activity deleted successfully"}