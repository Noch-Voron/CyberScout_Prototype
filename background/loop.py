import asyncio
from services.ingesta import ingesta

async def fetchLoop():
    while True:
        await ingesta()
        await asyncio.sleep(1800)