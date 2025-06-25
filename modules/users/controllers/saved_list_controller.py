from sqlalchemy.orm import Session
from modules.users.services import user_service

def get_saved_list(user_id: int, db: Session):
    return user_service.get_saved_list(user_id, db)

def save_activity_to_list(user_id: int, activity_id: int, db: Session):
    return user_service.add_activity_to_list(user_id, activity_id,db)

def remove_activity_from_list(user_id: int, save_id: int, db: Session):
    return user_service.remove_activity_from_list(user_id, save_id, db)