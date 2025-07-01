from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from sqlalchemy import select
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, joinedload
from config import settings
from utils.error_models import ErrorCode, create_error_response
from modules.users.constants import get_default_group, is_valid_group

from modules.users.services import cognito_service
from modules.trips.services import activities_service

COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID

def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.USER_ALREADY_EXISTS,
                "A user is already registered with this email."
            )
        )    
    cognito_user = cognito_service.sign_up(user, client)
    cognito_user_sub = cognito_user.get('UserSub')
 
    if user.cognito_group_id and not is_valid_group(user.cognito_group_id):
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.VALIDATION_ERROR,
                f"Invalid group: {user.cognito_group_id}. Valid groups are: GENERAL_USER, ADMIN"
            )
        )
    
    try:
        group_to_assign = user.cognito_group_id or get_default_group()
        client.admin_add_user_to_group(
            UserPoolId=COGNITO_USER_POOL_ID, 
            Username=user.email,
            GroupName=group_to_assign
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.USER_GROUP_ADDITION_FAILED,
                "Failed to add user to a group."
            )
        )
    
    new_user = User(
        email=user.email, 
        cognito_id=cognito_user_sub, 
        name=user.email.split('@')[0], 
        cognito_group_id=user.cognito_group_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

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


def get_user_by_cognito_id(cognito_id: str, db: Session) -> User | None:
    return db.execute(select(User).where(User.cognito_id == cognito_id)).scalar_one_or_none()
