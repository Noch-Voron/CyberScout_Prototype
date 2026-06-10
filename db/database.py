import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.pool = None
    async def connect(self):
        dataSource = os.getenv("dsn")
        if not dataSource:
            raise ValueError("Database enviroment variable not set")
        self.pool = await asyncpg.create_pool(dsn=dataSource)
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
    
db = Database()