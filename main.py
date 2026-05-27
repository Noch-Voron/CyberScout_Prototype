from fastapi import FastAPI, APIRouter
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from db.database import db

app = FastAPI()
router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(fetchLoop())
    db.connect("Insert dsn aqui")
    yield
    db.disconnect()