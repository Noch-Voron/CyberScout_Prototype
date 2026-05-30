from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict
from db.database import db
import json
from motor_de_cruce.motor import evaluar_noticia, activoServidor, noticiaEstructurada
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from db.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(fetchLoop())
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
router = APIRouter()

# Lo que envía react, este sería un inventario que se ingresa desde el frontend
class SolicitudSincronización(BaseModel):
    id_ultima_noticia: int
    inventario_local: List[activoServidor]


@app.post("/api/v1/sincronizar")
async def sincronizar_alertas(solicitud: SolicitudSincronización):
    alertas_totales =[]

    async with db.pool.acquire() as conn: # maybe habrá que cambiar esto.
        noticias_nuevas_db = await conn.fetch(
            "SELECT id, tags FROM noticias WHERE processed = TRUE and id >$1",
            solicitud.id_ultima_noticia
        ) # se seleccionan las id y tags de noticias donde no ha sido procesado por el cliente.
    
    if not noticias_nuevas_db:
        return {"nuevas_alertas": [], "id_último_sincronizado": solicitud.id_ultima_noticia}
    

    # transformar datos db a modelos.
    id_ultimo_procesado = solicitud.id_ultima_noticia

    for fila in noticias_nuevas_db:
        diccionario_noticia = json.loads(fila["tags"]) # unccoment if fila["tags"] es string
        noticia = noticiaEstructurada(**diccionario_noticia)

        alertas = evaluar_noticia(noticia, solicitud.inventario_local) # esta es la llamada al motor de cruce.
        if alertas:
            alertas_totales.extend(alertas)

        if fila["id"] > id_ultimo_procesado:
            id_ultimo_procesado = fila["id"]

    return {
        "nuevas_alertas": alertas_totales,
        "id_ultimo_sincronizado": id_ultimo_procesado
    }

