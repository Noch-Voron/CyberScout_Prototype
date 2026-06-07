from fastapi import FastAPI, APIRouter
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from db.database import db
from fastapi.middleware.cors import CORSMiddleware

from routers.noticias import router as noticias_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(fetchLoop())
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que cualquier HTML (o React de Yu) se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(noticias_router)

@app.get("/")
async def root():
    return {"message": "Motor de CyberScout Activo"}