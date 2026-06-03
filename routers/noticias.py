from fastapi import APIRouter, HTTPException
from db.database import db
import json
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