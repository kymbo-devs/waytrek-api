from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from sqlalchemy import desc, select
from modules.users.models.user import SavedList, User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session, joinedload

from modules.users.services import cognito_service
from modules.trips.services import activities_service


def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if (user_exists): raise HTTPException(400, "An user is already registered with this email.")
    cognito_user = cognito_service.sign_up(user, client)
    new_user = User(email=user.email, cognito_id=cognito_user.get(
        'UserSub'), name=user.email.split('@')[0])
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


def get_user_by_cognito_id(cognito_id: str, db: Session) -> User | None:
    return db.execute(select(User).where(User.cognito_id == cognito_id)).scalar_one_or_none()
