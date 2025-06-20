from sqlalchemy.orm import Session
from fastapi import status
from modules.users.services import user_service
from fastapi import HTTPException

def get_saved_list(user_cognito_id: str, db: Session):
    user = user_service.get_user_by_cognito_id(user_cognito_id, db)
    if (user == None): return []
    return user_service.get_saved_list(user.id, db)

def save_activity_to_list(user_cognito_id: str, activity_id: int, db: Session):
    user = user_service.get_user_by_cognito_id(user_cognito_id, db)
    if (user == None): raise HTTPException(status.HTTP_404_NOT_FOUND, "User doesn't exists")
    return user_service.add_activity_to_list(user.id, activity_id,db)