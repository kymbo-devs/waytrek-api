from sqlalchemy import Column
from db.session import Base
from sqlalchemy import Column, Integer, String

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String)
    nickname = Column(String)
    flag_url = Column(String)

    