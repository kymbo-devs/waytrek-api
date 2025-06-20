from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.services import user_service

def get_saved_list(user_cognito_id: str, db: Session):
    user = db.execute(select(User).where(User.cognito_id == user_cognito_id)).scalar_one_or_none()
    if (user == None): return []
    return user_service.get_saved_list(user.id, db)