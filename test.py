import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Cargar las variables de entorno (para leer tu dsn)
load_dotenv()

async def inyectar_noticia_prueba():
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(os.getenv("dsn"))
    
    
    titulo = "Vulnerabilidad Crítica en Servidores Linux V2"
    url = "https://cyberscout-test.com/alerta-linux-v2"
    texto_crudo = """
    Se ha detectado una nueva variante de la vulnerabilidad en servidores Linux. 
    Afecta a Ubuntu 22.04 y permite a los atacantes escalar privilegios a root. 
    CVE-2024-8888. Aplicar parche urgente.
    """
    
    await conn.execute("""
        INSERT INTO noticias (title, url, rawcontent, processed)
        VALUES ($1, $2, $3, FALSE)
    """, titulo, url, texto_crudo)
    
    print("Noticia de prueba inyectada con éxito en PostgreSQL.")
    print("¡Revisa la terminal donde está corriendo tu servidor FastAPI!")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(inyectar_noticia_prueba())