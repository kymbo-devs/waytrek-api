from pydantic import BaseModel
from typing import Optional


class TipBase(BaseModel):
    title: str
    content: str

class TipCreate(TipBase):
    pass
