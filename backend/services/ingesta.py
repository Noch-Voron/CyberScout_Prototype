import trafilatura
import feedparser
import httpx
import asyncio
from db.database import db

#hardcodeado mientras aun no este la hu3 con las fuentes dinamicas/disponibles en db
sources = ["https://feeds.feedburner.com/TheHackersNews"]

async def ingesta():
    print("ingesta")
#    for source in sources 
    feed = feedparser.parse(sources[0])
    for entry in feed.entries:
        async with db.pool.acquire() as conn:
            existing = await conn.fetchrow("SELECT 1 FROM noticias WHERE url = $1", entry.link)
            if not existing:
                async with httpx.AsyncClient() as client:
                    r = await(client.get(entry.link))
                    content = r.text
                clean = await asyncio.to_thread(trafilatura.extract, content, include_comments=False)
                print(clean)
                await conn.execute("INSERT INTO noticias (url, title, rawContent, processed) VALUES ($1,$2,$3,FALSE)", entry.link, entry.title, clean)
        return 0

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(ingesta())
    print(result)