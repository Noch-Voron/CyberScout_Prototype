from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from db.database import db
import json
from motor_de_cruce.motor import evaluar_noticia, activoServidor, noticiaEstructurada
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from services.ingesta import ingesta
from routers.noticias import app as noticias_routes
from routers.fuentes import app as fuentes_routes
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(fetchLoop())
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

#Para permitir el acceso desde el frontend en localhost:5173
origins = [
    'http://127.0.0.1:5173',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
    
app.include_router(noticias_routes, prefix="/api/noticias", tags=["Noticias"])
app.include_router(fuentes_routes, prefix="/api/fuentes", tags=["Fuentes"])


@app.get("/")
async def root():
    return {"message": "Motor de CyberScout Activo"}

# Lo que envía react, este sería un inventario que se ingresa desde el frontend
class SolicitudSincronización(BaseModel):
    id_ultima_noticia: int
    inventario_local: List[activoServidor]

@app.post("/api/v1/sincronizar")
async def sincronizar_alertas(solicitud: SolicitudSincronización):
    alertas_totales = []

    async with db.pool.acquire() as conn:
        noticias_nuevas_db = await conn.fetch(
            "SELECT id, title, url, rawcontent, tags, extractdate FROM noticias WHERE processed = TRUE and id > $1",
            solicitud.id_ultima_noticia
        )
    
    if not noticias_nuevas_db:
        return {"nuevas_alertas": [], "id_ultimo_sincronizado": solicitud.id_ultima_noticia}
    
    id_ultimo_procesado = solicitud.id_ultima_noticia

    for fila in noticias_nuevas_db:
        if not fila["tags"]:
            if fila["id"] > id_ultimo_procesado:
                id_ultimo_procesado = fila["id"]
            continue

        try:
            diccionario_noticia = json.loads(fila["tags"]) if isinstance(fila["tags"], str) else fila["tags"]
            noticia = noticiaEstructurada(**diccionario_noticia)

            alertas = evaluar_noticia(noticia, solicitud.inventario_local)
            for alerta in alertas:
                alerta_dict = alerta.model_dump()
                alerta_dict["noticia_id"] = fila["id"]
                alerta_dict["noticia_titulo"] = fila["title"]
                alerta_dict["noticia_url"] = fila["url"]
                alerta_dict["noticia_rawcontent"] = fila["rawcontent"]
                alerta_dict["noticia_extractdate"] = str(fila["extractdate"]) if fila["extractdate"] else None
                alertas_totales.append(alerta_dict)
        except Exception as e:
            print(f"Error procesando tags para noticia ID {fila['id']}: {e}")

        if fila["id"] > id_ultimo_procesado:
            id_ultimo_procesado = fila["id"]

    return {
        "nuevas_alertas": alertas_totales,
        "id_ultimo_sincronizado": id_ultimo_procesado
    }

