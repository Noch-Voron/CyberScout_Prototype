from fastapi import APIRouter
from db.database import db
from squemas.squemas import NoticiaData
import json

app = APIRouter()

@app.get("/", response_model= list[NoticiaData])
async def get_noticias():
    try:
        async with db.pool.acquire() as conn:
            noticias = await conn.fetch("SELECT id, title, url, rawcontent, tags, extractdate FROM noticias")
        aux = [NoticiaData(
                    id=noticia["id"], 
                    title=noticia["title"], 
                    url=noticia["url"], 
                    rawcontent=noticia["rawcontent"],
                    tags = json.loads(noticia["tags"]) if noticia["tags"] else None,
                    extractdate = noticia["extractdate"]
                ) for noticia in noticias]
        return aux
    except Exception as e:
        print("Error en get_noticias:", e)
        raise e

@app.get("/{noticia_id}", response_model= NoticiaData)
async def get_noticia_id(noticia_id: int):
    async with db.pool.acquire() as conn:
        noticia = await conn.fetchrow(
            "SELECT id, title, url, rawcontent, tags, extractdate FROM noticias WHERE id = $1",noticia_id)
        aux = NoticiaData(
                id=noticia["id"], 
                title=noticia["title"], 
                url=noticia["url"], 
                rawcontent=noticia["rawcontent"],
                tags = json.loads(noticia["tags"]) if noticia["tags"] else None,
                extractdate = noticia["extractdate"]
                )
    return aux
