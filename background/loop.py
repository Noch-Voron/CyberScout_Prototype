import asyncio
from services.ingesta import ingesta

async def fetchLoop():
    while True:
        ingesta()
        await asyncio.sleep(1800)