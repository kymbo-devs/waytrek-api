from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
from modules.tips.schemas.tip_schema import TipCreate

def create_tip(tip: TipCreate, db: Session = Depends(get_db)):
    return tip

def get_tip(tip_id: int, db: Session = Depends(get_db)):
    return {
        "id": 1,
        "title": "Test",
        "content": "Test"
    }
