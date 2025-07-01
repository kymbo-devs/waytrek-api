from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from modules.locations.schemas.location_schema import LocationCreate, LocationUpdate, LocationFilter
from modules.locations.models.location import Location
from utils.error_models import ErrorCode, create_error_response


def create_location(location: LocationCreate, db: Session):
    new_location = Location(
        country=location.country,
        city=location.city,
        nickname=location.nickname,
        flag_url=location.flag_url
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def get_location(location_id: int, db: Session):
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(
                ErrorCode.LOCATION_NOT_FOUND,
                f"Location with id {location_id} not found."
            )
        )
    return location


def get_locations(db: Session, filters: LocationFilter):
    query = db.query(Location)
    
    if filters.country is not None:
        query = query.filter(
            func.lower(Location.country).contains(filters.country.lower())
        )
    
    if filters.city is not None:
        query = query.filter(
            func.lower(Location.city).contains(filters.city.lower())
        )
    
    query = query.order_by(Location.city.asc())
    
    locations = query.offset(filters.skip).limit(filters.limit).all()
    return locations


def update_location(location_id: int, location_data: LocationUpdate, db: Session):
    location = get_location(location_id, db)
    
    update_data = location_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(location, key, value)
    
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def delete_location(location_id: int, db: Session):
    location = get_location(location_id, db)
    
    db.delete(location)
    db.commit()
    
    return {"detail": "Location deleted successfully"} 