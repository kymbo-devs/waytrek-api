
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate

def create_user(user: UserCreate, db: Session):
    return User(email=user.email, password=user.password)

def get_users():
     return [
          {
               "id": 1,
               "email": "test@test.com",
               "password": "test"
          }
     ]