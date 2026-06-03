from pydantic import BaseModel
from db.database import db

class Fuente(BaseModel):
    id: int
    url: str
    rawcontent: str
    
async def get_noticias_i():
    
    async with db.pool.acquire() as conn:
        noticias = await conn.fetch("SELECT id, title, url, rawcontent FROM noticias")
    aux = [Noticia(
                id=noticia["id"], 
                title=noticia["title"], 
                url=noticia["url"], 
                rawcontent=noticia["rawcontent"]
            ) for noticia in noticias]
    return aux