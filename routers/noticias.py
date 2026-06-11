from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from db.database import db
from squemas.squemas import NoticiaData
from services.notificador import notificador
import json
import asyncio

app = APIRouter()

@app.get("/", response_model= list[NoticiaData])
async def get_noticias():
    try:
        async with db.pool.acquire() as conn:
            noticias = await conn.fetch("SELECT id, title, url, rawcontent, tags, extractdate, processdate, processed FROM noticias")
        aux = [NoticiaData(
                    id=noticia["id"], 
                    title=noticia["title"], 
                    url=noticia["url"], 
                    rawcontent=noticia["rawcontent"],
                    tags = json.loads(noticia["tags"]) if noticia["tags"] else None,
                    extractdate = noticia["extractdate"],
                    processdate = noticia["processdate"], 
                    processed = noticia["processed"]
                ) for noticia in noticias]
        return aux
    except Exception as e:
        print("Error en get_noticias:", e)
        raise e

@app.get("/{noticia_id}", response_model= NoticiaData)
async def get_noticia_id(noticia_id: int):
    async with db.pool.acquire() as conn:
        noticia = await conn.fetchrow(
            "SELECT id, title, url, rawcontent, tags, extractdate, processdate, processed FROM noticias WHERE id = $1",noticia_id)
        aux = NoticiaData(
                id=noticia["id"], 
                title=noticia["title"], 
                url=noticia["url"], 
                rawcontent=noticia["rawcontent"],
                tags = json.loads(noticia["tags"]) if noticia["tags"] else None,
                extractdate = noticia["extractdate"],
                processdate = noticia["processdate"], 
                processed = noticia["processed"]
                )
    return aux

@app.get("/stream")
async def stream_noticias():
    async def event_generator():
        cola = await notificador.conectar_cliente()
        try:
            while True:
                alerta = await cola.get()
                yield f"data: {json.dumps(alerta)}\n\n"
        except asyncio.CancelledError:
            notificador.desconectar_cliente(cola)
        except Exception as e:
            notificador.desconectar_cliente(cola)
            print("Error en stream_noticias:", e)

@app.put("/{noticia_id}/reprocesar")
async def reprocesar_reporte(noticia_id: int):
    async with db.pool.acquire() as conn:
        await conn.execute("""
            UPDATE noticias 
            SET processed = FALSE
            WHERE id = $1
            """, noticia_id)
            
        return {"mensaje": "Noticia marcada para reprocesamiento"}

    return StreamingResponse(event_generator(), media_type="text/event-stream")
