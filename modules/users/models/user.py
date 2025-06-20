from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cognito_id = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    user_type_id = Column(Integer, ForeignKey("users_types.id", ondelete="cascade"))
    user_type: Mapped['UserType'] = relationship(back_populates="users")

class UserType(Base):
    __tablename__ = "users_types"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="user_type")


class SavedList(Base):
    __tablename__ = "saved_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    activity_id: Mapped[int] = mapped_column(ForeignKey('activities.id'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="saved_list")


User.saved_list = relationship(
    SavedList, back_populates="user", cascade="all, delete-orphan")
