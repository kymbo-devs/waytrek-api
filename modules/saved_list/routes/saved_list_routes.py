from typing import List
from fastapi import APIRouter
from fastapi import Depends
from db.session import get_db
from modules.saved_list.schemas.saved_list_schema import SaveActivityRequest, SavedList, SavedListWithActivity
from utils.auth_middleware import get_user_from_request
from modules.saved_list.controllers import saved_list_controller
from utils.error_models import (
    SavedListErrorResponse,
    ActivityNotFoundErrorResponse
)

router = APIRouter()

@router.get(
    "",
    summary="Get user saved list",
    description="Get authenticated user saved activities",
    response_model=List[SavedListWithActivity]
)
async def saved_list(db=Depends(get_db), user=Depends(get_user_from_request)):
    return saved_list_controller.get_saved_list(user.id, db)

@router.post(
    "",
    summary="Add activity to user list",
    description="Add a new activity to current user saved list",
    response_model=SavedList,
    responses={
        404: {"model": ActivityNotFoundErrorResponse, "description": "Activity or user not found"}
    }
)
async def add_saved_list(save_activity: SaveActivityRequest, db=Depends(get_db), user=Depends(get_user_from_request)):
    return saved_list_controller.save_activity_to_list(user.id, save_activity.activity_id, db)

@router.delete(
    "/{save_id}",
    summary="Remove activity from user list",
    description="Remove an activity from current user saved list",
    response_model=SavedList,
    responses={
        200: {"description": "Success response. Return deleted save"},
        404: {"model": SavedListErrorResponse, "description": "Save not found"},
        401: {"model": SavedListErrorResponse, "description": "User don't have permission to delete the save"},
    }
)
async def remove_from_saved_list(save_id: int, db=Depends(get_db), user=Depends(get_user_from_request)):
    return saved_list_controller.remove_activity_from_list(user.id, save_id, db)