from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import asyncio

from background.loop import fetchLoop


from db.database import db
from services.ingesta import ingesta
from routers.noticias import app as noticias_routes
from routers.fuentes import app as fuentes_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(fetchLoop())
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
router = APIRouter()

#Para permitir el acceso desde el frontend en localhost:5173
origins = [
    'http://127.0.0.1:5173',
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
    
app.include_router(noticias_routes, prefix="/api/noticias", tags=["Noticias"])
app.include_router(fuentes_routes, prefix="/api/fuentes", tags=["Fuentes"])


@app.get("/")
async def root():
    return {"message": "aaa"}

@app.post("/api/ingesta/")
async def run_ingesta():
    result = await ingesta()
    return {"status": "ok", "result": result}

