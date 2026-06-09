from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TagsData(BaseModel):
    categoria: str | None = None
    cve_id: str | None = None
    severidad: str | None = None
    activos_afectados: dict | None = None
    accion_recomendada: str | None = None
    puntuacion_cvss: str | None = None
    tipo_vulnerabilidad: str | None = None
    estado_vulnerabilidad: str | None = None
    
class NoticiaData(BaseModel):
    id: int
    title: str
    url: str
    rawcontent: str
    extractdate: datetime
    tags: Optional[TagsData] = None
    
class FuenteData(BaseModel):
    id: int
    url: str
    processdate: datetime
    processed: bool
    
class FuenteCreate(BaseModel):
    url: str