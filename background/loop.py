import asyncio
import os
from services.ingesta import ingesta
from services.procesador import procesar_noticias

async def fetchLoop():
    intervalo = int(os.getenv("FETCH_INTERVAL", 1800))
    while True:
        await ingesta()
        await procesar_noticias()
        await asyncio.sleep(intervalo)
