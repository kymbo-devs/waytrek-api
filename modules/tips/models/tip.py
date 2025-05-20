from sqlalchemy import Column, Integer, String
from db.session import Base


class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
  

    