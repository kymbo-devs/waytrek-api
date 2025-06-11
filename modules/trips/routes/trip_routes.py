from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from modules.trips.schemas.trip_schema import Activity, ActivityCreate, ActivityUpdate
from modules.trips.controllers.trip_controller import (
    create_trip as create_trip_controller, 
    get_trip as get_trip_controller,
    create_activity_controller,
    get_activities_controller,
    get_activity_controller,
    update_activity_controller,
    delete_activity_controller
)
from db.session import get_db

router = APIRouter()

@router.post(
    "/activities",
    response_model=Activity,
    status_code=201,
    summary="Create a new activity",
    description="Creates a new activity associated with a location, including details like history, tips, and media links.",
)
async def create_activity_route(activity: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity_controller(activity, db=db)

@router.get(
    "/activities",
    response_model=List[Activity],
    summary="List all activities",
    description="Retrieves a list of activities with optional filtering by location and active status, and supports pagination.",
)
async def get_activities_route(
    location_id: int | None = None,
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_activities_controller(
        db=db, skip=skip, limit=limit, location_id=location_id, is_active=is_active
    )

@router.get(
    "/activities/{activity_id}",
    response_model=Activity,
    summary="Get a specific activity",
    description="Retrieves detailed information about a single activity by its ID.",
)
async def get_activity_route(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_controller(activity_id, db)

@router.patch(
    "/activities/{activity_id}",
    response_model=Activity,
    summary="Update an activity",
    description="Updates the data of an existing activity. All fields are optional.",
)
async def update_activity_route(
    activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)
):
    return update_activity_controller(activity_id, activity, db)

@router.delete(
    "/activities/{activity_id}",
    status_code=204,
    summary="Delete an activity",
    description="Deletes an activity from the system by its ID.",
)
async def delete_activity_route(activity_id: int, db: Session = Depends(get_db)):
    delete_activity_controller(activity_id, db)
    return
