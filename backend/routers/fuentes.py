from fastapi import APIRouter, HTTPException

from db.database import db
from squemas.squemas import FuenteData, FuenteCreate

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
            processdate=fuente["processdate"],
            processed=fuente["processed"]
        )

    except Exception as e:
        print("Error en get_fuente_id:", e)
        raise e


@app.post("/", response_model=FuenteData)
async def add_fuente(fuente: FuenteCreate):

    async with db.pool.acquire() as conn:

        row = await conn.fetchrow("""
            INSERT INTO fuentes (url, processdate, processed)
            VALUES ($1, NOW(), FALSE)
            RETURNING id, url, processdate, processed
        """, fuente.url)

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