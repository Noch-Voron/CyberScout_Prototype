import trafilatura
import feedparser
import httpx
import asyncio
from db.database import db

#hardcodeado mientras aun no este la hu3 con las fuentes dinamicas/disponibles en db
sources = ["https://feeds.feedburner.com/TheHackersNews"]

async def ingesta():
    print("ingesta")
    
    async with db.pool.acquire() as conn:
        sources = await conn.fetch("SELECT url FROM fuentes WHERE processed = FALSE")
    for source in sources:
        feed = feedparser.parse(source["url"])

    #feed = feedparser.parse(sources[0]["url"])
        for entry in feed.entries:
            async with db.pool.acquire() as conn:
                existing = await conn.fetchrow("SELECT 1 FROM noticias WHERE url = $1", entry.link)
                if not existing:
                    async with httpx.AsyncClient() as client:
                        r = await(client.get(entry.link))
                        content = r.text
                    clean = await asyncio.to_thread(trafilatura.extract, content, include_comments=False)
                    #print(clean)
                    await conn.execute("INSERT INTO noticias (url, title, rawContent, processed) VALUES ($1,$2,$3,FALSE)", entry.link, entry.title, clean)
                else:
                    #las noticias son ordenadas de manera cronologica, si se encuentra uno ya procesado entonces todos los que estan detras ya estan procesados
                    print("Todas las noticias nuevas de"+ source["url"] +" han sido ingresadas")
                    break

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(ingesta())
    print(result)