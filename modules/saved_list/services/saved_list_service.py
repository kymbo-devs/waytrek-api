from fastapi import HTTPException, status
from sqlalchemy import desc, select
from modules.activities.services import activities_service
from modules.saved_list.models.saved_list import SavedList
from sqlalchemy.orm import Session, joinedload
from utils.error_models import ErrorCode, create_error_response

def get_saved_list(user_id: int, db: Session):
    result = db.execute(
        select(SavedList)
        .where(SavedList.user_id == user_id)
        .order_by(desc(SavedList.created_at))
        .options(joinedload(SavedList.activity))
    )
    return list(result.scalars().all())


def add_activity_to_list(user_id: int, activity_id: int, db: Session):
    existing_save = db.execute(
        select(SavedList)
        .where(SavedList.user_id == user_id)
        .where(SavedList.activity_id == activity_id)
    ).scalar_one_or_none()
    if (existing_save): return existing_save
    activity = activities_service.get_activity(activity_id, db)
    saved_activity = SavedList(
        user_id=user_id,
        activity_id=activity.id
    )
    db.add(saved_activity)
    db.commit()
    db.refresh(saved_activity)
    return saved_activity

def remove_activity_from_list(user_id: int, save_id: int, db: Session):
    existing_save = db.execute(
        select(SavedList)
        .where(SavedList.id == save_id)
    ).scalar_one_or_none()
    if (existing_save == None): 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=create_error_response(
                ErrorCode.SAVE_NOT_FOUND,
                f"Save with id {save_id} not found"
            )
        )
    if (existing_save.user_id != user_id): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=create_error_response(
                ErrorCode.UNAUTHORIZED_DELETE,
                f"This user can't delete this save"
            )
        )
    db.delete(existing_save)
    db.commit()
    return existing_save
