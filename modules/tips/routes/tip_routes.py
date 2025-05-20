from fastapi import APIRouter
from modules.tips.schemas.tip_schema import TipCreate
from modules.tips.controllers.tip_controller import create_tip, get_tip

router = APIRouter()

@router.post("/tips")
async def create_tip(tip: TipCreate):
    return create_tip(tip)

@router.get("/tips/{tip_id}")
async def get_tip(tip_id: int):
    return get_tip(tip_id)
