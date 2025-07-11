from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship, Mapped
from db.session import Base
from modules.users.constants import CognitoGroup


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cognito_id = Column(String, nullable=False, unique=True)
    cognito_group_id = Column(String, nullable=False, server_default=CognitoGroup.GENERAL_USER.value)
    is_active = Column(Boolean, default=True)
    user_type_id = Column(Integer, ForeignKey("users_types.id", ondelete="cascade"))
    user_type: Mapped['UserType'] = relationship(back_populates="users")

class UserType(Base):
    __tablename__ = "users_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="user_type")
