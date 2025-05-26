
from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    user = User(email=user.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.execute(select(User)).scalars().all()
