import trafilatura
import feedparser
import httpx
import asyncio

#hardcodeado mientras aun no este la hu3 con las fuentes dinamicas/disponibles en db
sources = ["https://feeds.feedburner.com/TheHackersNews"]



async def ingesta():
#    for source in sources 
    feed = feedparser.parse(sources[0])
    for entry in feed.entries:
#        if entry.link in db: continue 
        async with httpx.AsyncClient() as client:
            r = await(client.get(entry.link))
            content = r.text
        clean = await asyncio.to_thread(trafilatura.extract, content, include_comments=False)
        print(clean)
#        db.insert(content)
    return 0

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(ingesta())
    print(result)