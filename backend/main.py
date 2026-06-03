from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from background.loop import fetchLoop
import asyncio
from contextlib import asynccontextmanager
from db.database import db
from services.ingesta import ingesta
from services.noticias import Noticia, get_noticias_i

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
    
@app.get("/")
async def root():
    return {"message": "aaa"}

@app.post("/api/ingesta/")
async def run_ingesta():
    result = await ingesta()
    return {"status": "ok", "result": result}

@app.get("/api/noticias/", response_model= list[Noticia])
async def get_noticias():
    try:
        result = await get_noticias_i()
        return result
    except Exception as e:
        print("Error en get_noticias:", e)
        raise e

