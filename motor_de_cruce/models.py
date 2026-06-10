from pydantic import BaseModel
from typing import List, Dict

class activoServidor(BaseModel):
    nombre: str
    id: str
    entorno: str #tipo si es linux (goated) o windows 10, 11 (trash)
    software_instalado: Dict[str,str] # "Linux Fedora": "42"


# aqui viene lo que entregaría la T3
class softwareVulnerable(BaseModel):
    nombre: str
    versiones_afectadas: List[str] # como ["1.4.6", "5.x", etc]


class noticiaEstructurada(BaseModel):
    cve_id: str | None # por si no hay (caso mayoritorio según entiendo)
    severidad: str # tipo crítico, alto, medio, bajo
    activos_afectados: Dict[str, List[str]] # Linux Fedora: [42,43,44]
    acción_recomendada: str = "" # borrar si no se hace
    puntuacion_cvss: str | None = None
    tipo_vulnerabilidad: str | None = None # none en caso de que no sea claro
    estado_vulnerabilidad: str = "" # como, sin parche o con parche, etc. 

    # Respecto a este, pienso que podría ser importante el mantener una id única y asociable a una misma vulnerabilidad, y dado que potencialmente puede mejorar o empeorar la situación se tendría que actualizar la info respecto a esa. No sé solo una idea.


class alertaGenerada(BaseModel):
    id_servidor:str
    nombre_servidor:str
    software_afectado:str
    nivel_match:str # partial, full o none
    noticia_original: noticiaEstructurada