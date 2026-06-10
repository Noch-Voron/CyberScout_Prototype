import asyncio
# pyrefly: ignore [missing-import]
import asyncpg
import os
import json
from dotenv import load_dotenv

load_dotenv()

# 3 Mock news articles already "processed" by Gemini (processed = True and tags populated)
mock_news = [
    # --- 1 NO AFECTADO (NO-MATCH) ---
    {
        "title": "Inyección SQL Crítica en MySQL Server (CVE-2024-MYSQL-701)",
        "url": "https://seguridad.example.com/cve-2024-mysql-auth",
        "rawcontent": "Una vulnerabilidad en el protocolo de autenticación de MySQL Server en versiones 8.0.x permite a un atacante enviar paquetes manipulados y realizar una inyección SQL antes de que el servidor valide las credenciales.",
        "tags": {}
    },

    # --- 1 COINCIDENCIA PARCIAL (PARTIAL-MATCH) ---
    {
        "title": "Desbordamiento de enteros en Python (CVE-2024-PYTHON-311)",
        "url": "https://seguridad.example.com/cve-2024-python-integer-overflow",
        "rawcontent": "Se ha identificado un desbordamiento de enteros en la biblioteca estándar de Python (específicamente en el módulo decimal) que afecta a las versiones de la rama 3.11 en adelante (>=3.11.0). No afecta a la versión 3.10.",
        "tags": {}
    },

    # --- 1 COINCIDENCIA COMPLETA (FULL-MATCH) ---
    {
        "title": "Fallo de denegación de servicio en PostgreSQL 15.2.x (CVE-2024-PG-152)",
        "url": "https://seguridad.example.com/cve-2024-postgres-dos-152",
        "rawcontent": "Un fallo de denegación de servicio (DoS) afecta directamente a PostgreSQL versión 15.2.0 al procesar consultas recursivas con operadores complejos. Provoca un crash inmediato del proceso de base de datos.",
        "tags": {}
    }
]

async def inyectar_mock_news():
    dsn = os.getenv("dsn")
    if not dsn:
        print("Error: No se encontró la variable 'dsn' en el archivo .env")
        return
        
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(dsn)
    
    print(f"Inyectando {len(mock_news)} noticias de prueba pre-procesadas...")
    
    exito = 0
    errores = 0
    
    for news in mock_news:
        try:
            # Serializar las etiquetas estructuradas a JSON
            tags_json = json.dumps(news["tags"])
            
            await conn.execute("""
                INSERT INTO noticias (title, url, rawcontent, processed, tags, extractdate, processdate)
                VALUES ($1, $2, $3, TRUE, $4, NOW(), NOW())
                ON CONFLICT (url) DO NOTHING
            """, news["title"], news["url"], news["rawcontent"], tags_json)
            exito += 1
        except Exception as e:
            print(f"Error inyectando noticia '{news['title']}': {e}")
            errores += 1

    print(f"\nProceso finalizado. {exito} noticias inyectadas con éxito (o ya existían), {errores} errores.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(inyectar_mock_news())
