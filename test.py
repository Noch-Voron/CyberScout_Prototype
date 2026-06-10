import asyncio
# pyrefly: ignore [missing-import]
import asyncpg
import os
from dotenv import load_dotenv

# Cargar las variables de entorno (para leer tu dsn)
load_dotenv()

async def inyectar_noticia_prueba():
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(os.getenv("dsn"))
    
    
    titulo = "Vulnerabilidad Zero-Day en Apache (Path Traversal)"
    url = "https://cyberscout-test.com/alerta-apache-cve-2021-41773"
    texto_crudo = """
    CISA y expertos en ciberseguridad han detectado explotación activa de una vulnerabilidad 
    crítica de Path Traversal (CVE-2021-41773) en Apache HTTP Server. 
    Esta falla afecta específicamente a la versión 2.4.49 y permite a un atacante no autenticado 
    leer archivos arbitrarios del sistema e incluso ejecutar código remoto (RCE).
    Urge actualizar los servidores afectados inmediatamente.
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