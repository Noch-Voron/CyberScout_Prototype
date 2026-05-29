import asyncio
from services.ingesta import ingesta
from services.procesador import procesar_noticias

async def fetchLoop():
    while True:
        await ingesta()
        await procesar_noticias()
        await asyncio.sleep(1800)
