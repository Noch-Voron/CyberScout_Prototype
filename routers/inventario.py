from fastapi import APIRouter
from motor_de_cruce.motor import Inventario_Local

router = APIRouter()

@router.get("/api/inventario")
async def obtener_inventario():
    # FastAPI convertirá automáticamente tu lista de objetos Pydantic a JSON
    return Inventario_Local