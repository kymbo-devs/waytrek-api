from sqlalchemy.orm import Session
from modules.saved_list.services import saved_list_service

def get_saved_list(user_id: int, db: Session):
    return saved_list_service.get_saved_list(user_id, db)

def save_activity_to_list(user_id: int, activity_id: int, db: Session):
    return saved_list_service.add_activity_to_list(user_id, activity_id,db)

def remove_activity_from_list(user_id: int, save_id: int, db: Session):
    return saved_list_service.remove_activity_from_list(user_id, save_id, db)