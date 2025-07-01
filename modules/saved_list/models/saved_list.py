from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from db.session import Base
from modules.activities.models.activity import Activity
from modules.users.models.user import User



class SavedList(Base):
    __tablename__ = "saved_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    activity_id: Mapped[int] = mapped_column(ForeignKey('activities.id'))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="saved_list")
    activity: Mapped["Activity"] = relationship()


User.saved_list = relationship(
    SavedList, back_populates="user", cascade="all, delete-orphan")
