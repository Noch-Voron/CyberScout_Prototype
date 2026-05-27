import asyncpg

class Database:
    def __init__(self):
        self.pool = None
    async def connect(self, dataSource: str):
        self.pool = await asyncpg.create_pool(dsn=dataSource)
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
    
db = Database()