from fastapi import APIRouter, HTTPException
import feedparser

from db.database import db
from squemas.squemas import FuenteData, FuenteCreate
from services.ingesta import ingesta

app = APIRouter()
    
@app.get("/", response_model=list[FuenteData])
async def get_fuentes():
    try:
        async with db.pool.acquire() as conn:
            fuentes = await conn.fetch(
                """
                SELECT id, url, processdate, processed
                FROM fuentes
                ORDER BY id
                """
            )

        return [
            FuenteData(
                id=f["id"],
                url=f["url"],
                processdate=f["processdate"],
                processed=f["processed"]
            )
            for f in fuentes
        ]

    except Exception as e:
        print("Error en get_fuentes:", e)
        raise e
    
@app.get("/{fuente_id}", response_model=FuenteData)
async def get_fuente_id(fuente_id: int):
    try:
        async with db.pool.acquire() as conn:
            fuente = await conn.fetchrow(
                """
                SELECT id, url, processdate, processed
                FROM fuentes
                WHERE id = $1
                """,
                fuente_id
            )

        if fuente is None:
            raise HTTPException(
                status_code=404,
                detail="Fuente no encontrada"
            )

        return FuenteData(
            id=fuente["id"],
            url=fuente["url"],
            processdate = fuente["processdate"],
            processed=fuente["processed"]
        )

    except Exception as e:
        print("Error en get_fuente_id:", e)
        raise e


import requests
import feedparser


def validar_feed(url: str):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "CyberScout/1.0"
            }
        )

    except requests.exceptions.SSLError:
        return False, "La fuente posee un certificado SSL inválido."

    except requests.exceptions.ConnectionError:
        return False, "No fue posible conectar con la fuente."

    except requests.exceptions.Timeout:
        return False, "La fuente tardó demasiado en responder."

    except requests.exceptions.RequestException as e:
        return False, f"Error al acceder a la fuente: {str(e)}"

    if response.status_code >= 400:
        return False, f"La fuente respondió con código {response.status_code}."

    try:
        feed = feedparser.parse(response.content)

        tiene_feed = (
            len(feed.entries) > 0
            or feed.feed.get("title")
        )

        if not tiene_feed:
            return False, "No se detectó un feed RSS/Atom válido."

        return True, "Feed válido"

    except Exception:
        return False, "No fue posible procesar el feed."


@app.post("/", response_model=FuenteData)
async def add_fuente(fuente: FuenteCreate):
    
    # Validar RSS
    es_valido, mensaje = validar_feed(fuente.url)

    if not es_valido:
        raise HTTPException(
            status_code=400,
            detail=mensaje
        )


    async with db.pool.acquire() as conn:

        row = await conn.fetchrow("""
            INSERT INTO fuentes (url, processdate, processed)
            VALUES ($1, NOW(), FALSE)
            ON CONFLICT (url) DO NOTHING
            RETURNING id, url, processdate, processed
        """, fuente.url)
        
        if row is None:
            raise HTTPException(
                status_code=409,
                detail="La fuente ya se encuentra registrada."
            )
        
    await ingesta()
    return FuenteData(
        id=row["id"],
        url=row["url"],
        processdate=row["processdate"],
        processed=row["processed"]
    )



@app.delete("/{fuente_id}", response_model= int)
async def delete_fuente(fuente_id: int):
    try:
        async with db.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM fuentes WHERE id = $1", 
                (fuente_id)
                )
        return fuente_id
    except Exception as e:
        print("Error en add_fuente:", e)
        raise e


@app.put("/{fuente_id}/toggle", response_model=FuenteData)
async def toggle_fuente(fuente_id: int):
    try:
        async with db.pool.acquire() as conn:

            row = await conn.fetchrow(
                """
                UPDATE fuentes
                SET processed = NOT processed
                WHERE id = $1
                RETURNING
                    id,
                    url,
                    processdate,
                    processed
                """,
                fuente_id
            )

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Fuente no encontrada"
            )

        return FuenteData(
            id=row["id"],
            url=row["url"],
            processdate=row["processdate"],
            processed=row["processed"]
        )

    except Exception as e:
        print("Error en toggle_fuente:", e)
        raise e