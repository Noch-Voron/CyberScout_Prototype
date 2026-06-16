import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# 4 Unprocessed news articles (processed = False, tags = NULL)
# Designed to be processed by Gemini and evaluated against the inventory.
unprocessed_news = [
    # --- 1 MATCH FULL (Apache 2.4.49 - matches SRV-LEGACY-WIN) ---
    {
        "title": "Critical Remote Code Execution in Apache HTTP Server 2.4.49",
        "url": "https://seguridad.example.com/noticia-apache-critical-2449",
        "rawcontent": "A major zero-day vulnerability (CVE-2021-41773) has been discovered in Apache HTTP Server. It specifically affects version 2.4.49. Attackers can exploit a path traversal flaw to read arbitrary server files or execute remote code with daemon privileges."
    },

    # --- 1 MATCH PARCIAL PARA AMBOS SERVERS (PostgreSQL 13.x y 14.x) ---
    # Ambos servidores tienen postgresql (15.2.0 y 11.5.0).
    # Como la noticia afecta a postgresql pero a las ramas 13/14, generará un match parcial en ambos.
    {
        "title": "SQL Injection vulnerability patched in PostgreSQL 13 and 14 branches",
        "url": "https://seguridad.example.com/noticia-postgres-sql-injection-13-14",
        "rawcontent": "A security release has been issued for PostgreSQL database engine. The update addresses a SQL injection vulnerability that affects all versions in the PostgreSQL 13.x and PostgreSQL 14.x branches. Systems running PostgreSQL 11 or PostgreSQL 15 are not affected by this vulnerability."
    },

    # --- 2 SIN MATCH (Cisco IOS y WordPress) ---
    {
        "title": "Cisco releases critical updates for IOS XE web interface vulnerability",
        "url": "https://seguridad.example.com/noticia-cisco-ios-xe-webui",
        "rawcontent": "Cisco has released patches for a critical vulnerability in the web user interface (WebUI) of Cisco IOS XE software. This flaw allows unauthenticated remote attackers to create account databases with administrative access."
    },
    {
        "title": "WordPress 6.4.2 security patch fixes critical remote code execution",
        "url": "https://seguridad.example.com/noticia-wordpress-rce-642",
        "rawcontent": "The WordPress security team has released version 6.4.2 to address a critical vulnerability in the WordPress Core. A deserialization chain could lead to remote code execution in combinations with certain plugins."
    }
]

async def inyectar_unprocessed_news():
    dsn = os.getenv("dsn")
    if not dsn:
        print("Error: No se encontró la variable 'dsn' en el archivo .env")
        return
        
    print("Conectando a la base de datos...")
    conn = await asyncpg.connect(dsn)
    
    print(f"Inyectando {len(unprocessed_news)} noticias NO procesadas...")
    
    exito = 0
    errores = 0
    
    for news in unprocessed_news:
        try:
            await conn.execute("""
                INSERT INTO noticias (title, url, rawcontent, processed, tags, extractdate, processdate)
                VALUES ($1, $2, $3, FALSE, NULL, NOW(), NULL)
                ON CONFLICT (url) DO NOTHING
            """, news["title"], news["url"], news["rawcontent"])
            exito += 1
        except Exception as e:
            print(f"Error inyectando noticia '{news['title']}': {e}")
            errores += 1

    print(f"\nProceso finalizado. {exito} noticias inyectadas con éxito (o ya existían), {errores} errores.")
    print("Para procesarlas, ejecuta o inicia el script 'procesador.py' o levanta tu servidor FastAPI.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(inyectar_unprocessed_news())
