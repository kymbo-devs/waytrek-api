from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from modules.locations.controllers.location_controller import (
    create_location_controller,
    get_locations_controller,
    get_location_controller,
    update_location_controller,
    delete_location_controller
)
from modules.locations.schemas.location_schema import Location, LocationCreate, LocationUpdate, LocationFilter
from db.session import get_db
from utils.error_models import (
    LocationNotFoundErrorResponse,
    ValidationErrorResponse,
    ServerErrorResponse
)

router = APIRouter()

@router.post(
    "",
    response_model=Location,
    status_code=status.HTTP_201_CREATED,
    responses={
        500: {"model": ServerErrorResponse, "description": "Internal server error"}
    },
    summary="Create a new location",
    description="""
    Creates a new location.
    
    Required fields:
    - country: The name of the country
    - city: The name of the city
    - nickname: A friendly name for the location
    - flag_url: URL to the country's flag image
    """,
)
async def create_location_route(location: LocationCreate, db: Session = Depends(get_db)):
    return create_location_controller(location, db=db)


@router.get(
    "",
    response_model=List[Location],
    summary="List all locations",
    description="""
    Retrieves a list of all locations with optional filtering and pagination.
    
    Available filters:
    - country: Filter by country name (partial match, case insensitive)
    - city: Filter by city name (partial match, case insensitive)
    - skip: Number of records to skip for pagination (default: 0)
    - limit: Maximum number of records to return (default: 100)
    
    Results are automatically sorted alphabetically by city name.
    """,
)
async def get_locations_route(
    filters: LocationFilter = Depends(),
    db: Session = Depends(get_db),
):
    return get_locations_controller(filters=filters, db=db)


@router.get(
    "/{location_id}",
    response_model=Location,
    responses={
        404: {"model": LocationNotFoundErrorResponse, "description": "Location not found"},
        500: {"model": ServerErrorResponse, "description": "Internal server error"}
    },
    summary="Get a specific location",
    description="Retrieves detailed information about a single location by its ID.",
)
async def get_location_route(location_id: int, db: Session = Depends(get_db)):
    return get_location_controller(location_id, db)


@router.put(
    "/{location_id}",
    response_model=Location,
    responses={
        404: {"model": LocationNotFoundErrorResponse, "description": "Location not found"},
        500: {"model": ServerErrorResponse, "description": "Internal server error"}
    },
    summary="Update a location",
    description="""
    Updates the information of an existing location. All fields are optional.
    
    Fields that can be updated:
    - country: The name of the country
    - city: The name of the city
    - nickname: A friendly name for the location
    - flag_url: URL to the country's flag image
    
    Only the fields provided in the request will be updated.
    """,
)
async def update_location_route(
    location_id: int, 
    location: LocationUpdate, 
    db: Session = Depends(get_db)
):
    return update_location_controller(location_id, location, db)


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": LocationNotFoundErrorResponse, "description": "Location not found"},
        500: {"model": ServerErrorResponse, "description": "Internal server error"}
    },
    summary="Delete a location",
    description="""
    Deletes a location from the system by its ID.
    
    Warning: This operation is irreversible. Make sure the location is not being 
    referenced by any activities before deletion to avoid data integrity issues.
    """,
)
async def delete_location_route(location_id: int, db: Session = Depends(get_db)):
    delete_location_controller(location_id, db)
    return 