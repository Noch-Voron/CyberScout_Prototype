from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from db.database import db
import json
import asyncio
from services.notificador import notificador
router = APIRouter(prefix="/api/noticias", tags=["Auditoría de Noticias"])

@router.get("/procesadas")
async def obtener_noticias_procesadas():
    if not db.pool:
        raise HTTPException(status_code=500, detail="La base de datos no está conectada.")

    try:
        async with db.pool.acquire() as conn:
            # Traemos las noticias procesadas ordenadas por la más reciente
            resultados = await conn.fetch("""
                SELECT id, title, url, rawcontent, tags, processdate 
                FROM noticias 
                WHERE processed = TRUE 
                ORDER BY processdate DESC
            """)
            
            # Formateamos los registros de asyncpg (Record) a una lista normal de Python
            noticias_audit = []
            for row in resultados:
                noticias_audit.append({
                    "id": row["id"],
                    "title": row["title"],
                    "url": row["url"],
                    "rawcontent": row["rawcontent"],
                    # Si 'tags' viene como texto (string), lo convertimos a JSON real
                    "tags": json.loads(row["tags"]) if isinstance(row["tags"], str) else row["tags"],
                    "processdate": row["processdate"]
                })
                
            return noticias_audit

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los datos: {str(e)}")

@router.get("/stream")
async def stream_noticias(request: Request):
    """
    Endpoint SSE: Mantiene la conexión abierta y empuja noticias en tiempo real.
    """
    async def generador_eventos():
        cola_cliente = await notificador.conectar_cliente()
        try:
            while True:
                # Si el cliente cierra el navegador, salimos del loop
                if await request.is_disconnected():
                    break
                
                # Esperamos hasta que haya una nueva noticia en la cola
                nueva_noticia = await cola_cliente.get()
                
                # El formato "data: {json}\n\n" es el estándar obligatorio para SSE
                yield f"data: {json.dumps(nueva_noticia)}\n\n"
                
        except asyncio.CancelledError:
            pass
        finally:
            notificador.desconectar_cliente(cola_cliente)

    return StreamingResponse(generador_eventos(), media_type="text/event-stream")