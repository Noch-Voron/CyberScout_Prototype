import json

from db.database import db
from services.classifier import classify_article

async def procesar_noticias():

    async with db.pool.acquire() as conn:

        noticias = await conn.fetch("""
            SELECT id, rawcontent
            FROM noticias
            WHERE processed = FALSE
        """)

        for noticia in noticias:

            tags = await clasificar_noticias(
                noticia["rawcontent"]
            )

            await conn.execute(
                """
                UPDATE noticias
                SET
                    tags = $1::json,
                    processed = TRUE,
                    processdate = CURRENT_TIMESTAMP
                WHERE id = $2
                """,
                json.dumps(tags),
                noticia["id"]
            )
