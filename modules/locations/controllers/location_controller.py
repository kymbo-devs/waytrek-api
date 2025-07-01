from sqlalchemy.orm import Session
from modules.locations.schemas.location_schema import LocationCreate, LocationUpdate, LocationFilter
from modules.locations.services import location_service


def create_location_controller(location: LocationCreate, db: Session):
    return location_service.create_location(location, db)


def get_locations_controller(filters: LocationFilter, db: Session):
    return location_service.get_locations(db=db, filters=filters)


def get_location_controller(location_id: int, db: Session):
    return location_service.get_location(location_id=location_id, db=db)


def update_location_controller(location_id: int, location_data: LocationUpdate, db: Session):
    return location_service.update_location(location_id=location_id, location_data=location_data, db=db)


def delete_location_controller(location_id: int, db: Session):
    return location_service.delete_location(location_id=location_id, db=db) 