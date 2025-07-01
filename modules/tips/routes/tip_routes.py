from fastapi import APIRouter
from modules.tips.schemas.tip_schema import TipCreate
from modules.tips.controllers import tip_controller

router = APIRouter()

@router.post("")
async def create_tip(tip: TipCreate):
    return tip_controller.create_tip(tip)

@router.get("/{tip_id}")
async def get_tip(tip_id: int):
    return tip_controller.get_tip(tip_id)
