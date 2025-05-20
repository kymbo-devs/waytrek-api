from fastapi import APIRouter
from modules.trips.schemas.trip_schema import TripCreate
from modules.trips.controllers.trip_controller import create_trip, get_trip

router = APIRouter()

@router.post("/trips")
async def create_trip(trip: TripCreate):
    return create_trip(trip)

@router.get("/trips/{trip_id}")
async def get_trip(trip_id: int):
    return get_trip(trip_id)
