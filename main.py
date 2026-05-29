from fastapi import FastAPI, APIRouter
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from db.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(fetchLoop())
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
router = APIRouter()

@app.get("/")
async def root():
    return {"message": "aaa"}