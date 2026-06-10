import asyncio
# pyrefly: ignore [missing-import]
import asyncpg
import os
import json
from dotenv import load_dotenv

load_dotenv()

# 10 Mock news articles already "processed" by Gemini (processed = True and tags populated)
mock_news = [
    # --- 4 NO AFECHADOS (NO-MATCH) ---
    {
        "title": "Vulnerabilidad en Docker Engine permite evasión de contenedor",
        "url": "https://seguridad.example.com/cve-2024-docker-escape",
        "rawcontent": "Se ha descubierto un fallo crítico en Docker Engine en versiones anteriores a la 20.10.0 que permite la evasión de contenedor (escape) hacia el host. Se recomienda encarecidamente actualizar.",
        "tags": {
            "cve_id": "CVE-2024-DOCKER-001",
            "severidad": "Crítico",
            "activos_afectados": {"docker": ["<20.10.0"]},
            "acción_recomendada": "Actualizar Docker Engine a la última versión disponible.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Container Escape",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Fallo de denegación de servicio en OpenSSL 3.0",
        "url": "https://seguridad.example.com/cve-2024-openssl-dos",
        "rawcontent": "Una vulnerabilidad en el parseo de certificados en OpenSSL versiones 3.0.x puede provocar una denegación de servicio (DoS) mediante el consumo infinito de ciclos de CPU.",
        "tags": {
            "cve_id": "CVE-2024-OPENSSL-002",
            "severidad": "Alto",
            "activos_afectados": {"openssl": ["3.0.x"]},
            "acción_recomendada": "Aplicar parches proporcionados por su distribución.",
            "puntuacion_cvss": "7.5",
            "tipo_vulnerabilidad": "Denial of Service",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Escalada de privilegios en el Kernel de Windows",
        "url": "https://seguridad.example.com/cve-2024-windows-kernel-privesc",
        "rawcontent": "Microsoft advierte sobre una vulnerabilidad local de escalada de privilegios en el kernel de Windows. Un atacante con acceso básico podría obtener privilegios de SYSTEM.",
        "tags": {
            "cve_id": "CVE-2024-MSFT-1032",
            "severidad": "Alto",
            "activos_afectados": {"windows_kernel": ["10.*"]},
            "acción_recomendada": "Instalar el parche acumulativo de Windows Update.",
            "puntuacion_cvss": "7.8",
            "tipo_vulnerabilidad": "Privilege Escalation",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Exposición de secretos en Kubernetes Dashboard",
        "url": "https://seguridad.example.com/cve-2024-k8s-dashboard",
        "rawcontent": "El dashboard oficial de Kubernetes en versiones 1.24.x filtra tokens de acceso en los logs del servidor bajo configuraciones específicas. Esto puede llevar a la apropiación de clusters.",
        "tags": {
            "cve_id": "CVE-2024-K8S-004",
            "severidad": "Medio",
            "activos_afectados": {"kubernetes": ["1.24.*"]},
            "acción_recomendada": "Actualizar a Kubernetes Dashboard 1.25 o superior.",
            "puntuacion_cvss": "6.5",
            "tipo_vulnerabilidad": "Information Disclosure",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },

    # --- 3 COINCIDENCIAS PARCIALES (PARTIAL-MATCH) ---
    {
        "title": "Vulnerabilidad en Nginx 1.21.x / 1.22.x (HTTP/2 Rapid Reset)",
        "url": "https://seguridad.example.com/cve-2024-nginx-rapid-reset",
        "rawcontent": "Se ha reportado que Nginx en sus versiones de desarrollo 1.21.x y 1.22.x es vulnerable al ataque HTTP/2 Rapid Reset, permitiendo ataques de denegación de servicio distribuidos (DDoS).",
        "tags": {
            "cve_id": "CVE-2024-NGINX-202",
            "severidad": "Medio",
            "activos_afectados": {"nginx": ["1.21.x", "1.22.x"]},
            "acción_recomendada": "Actualizar a la versión estable 1.24 o deshabilitar HTTP/2 temporalmente.",
            "puntuacion_cvss": "5.3",
            "tipo_vulnerabilidad": "Denial of Service",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Fuga de memoria en Oracle Java SE (versiones 17 y 21)",
        "url": "https://seguridad.example.com/cve-2024-java-leak",
        "rawcontent": "El componente de serialización en Oracle Java SE 17.x y 21.x presenta una fuga de memoria que puede degradar el rendimiento de servidores de aplicaciones críticas.",
        "tags": {
            "cve_id": "CVE-2024-JAVA-901",
            "severidad": "Bajo",
            "activos_afectados": {"java": ["==17.*", "==21.*"]},
            "acción_recomendada": "Aplicar el último Java CPU update.",
            "puntuacion_cvss": "3.5",
            "tipo_vulnerabilidad": "Memory Leak",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Inyección SQL en PostgreSQL (versiones 12 a 14)",
        "url": "https://seguridad.example.com/cve-2024-postgres-sql-inject",
        "rawcontent": "Un fallo de inyección SQL afecta a PostgreSQL en sus ramas obsoletas 12.x, 13.x y 14.x a través de funciones integradas mal saneadas. No afecta a las versiones 11 o 15.",
        "tags": {
            "cve_id": "CVE-2024-PG-4022",
            "severidad": "Alto",
            "activos_afectados": {"postgresql": [">=12.0.0, <15.0.0"]},
            "acción_recomendada": "Actualizar a las versiones parcheadas de mantenimiento de PostgreSQL.",
            "puntuacion_cvss": "8.1",
            "tipo_vulnerabilidad": "SQL Injection",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },

    # --- 3 COINCIDENCIAS COMPLETAS (FULL-MATCH) ---
    {
        "title": "Ejecución remota de código en Nginx 1.18.0 y anteriores",
        "url": "https://seguridad.example.com/cve-2024-nginx-rce",
        "rawcontent": "Una vulnerabilidad de desbordamiento de búfer en Nginx versión 1.18.0 y anteriores permite a un atacante remoto ejecutar comandos en el servidor mediante peticiones HTTP maliciosas.",
        "tags": {
            "cve_id": "CVE-2024-NGINX-118",
            "severidad": "Crítico",
            "activos_afectados": {"nginx": ["<1.20.0"]},
            "acción_recomendada": "Actualizar Nginx inmediatamente.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Remote Code Execution",
            "estado_vulnerabilidad": "Sin Parche"
        }
    },
    {
        "title": "CISA advierte sobre explotación de Path Traversal en Apache 2.4.49",
        "url": "https://seguridad.example.com/cve-2021-41773-apache",
        "rawcontent": "Se detectó explotación activa de una vulnerabilidad de Path Traversal crítica en Apache HTTP Server 2.4.49 que permite lectura de archivos del sistema e inyección de comandos.",
        "tags": {
            "cve_id": "CVE-2021-41773",
            "severidad": "Crítico",
            "activos_afectados": {"apache": ["2.4.49"]},
            "acción_recomendada": "Actualizar a Apache HTTP Server 2.4.50 de inmediato.",
            "puntuacion_cvss": "9.8",
            "tipo_vulnerabilidad": "Path Traversal / RCE",
            "estado_vulnerabilidad": "Parche Disponible"
        }
    },
    {
        "title": "Fallo crítico de autenticación en PostgreSQL (15.x y 11.x)",
        "url": "https://seguridad.example.com/cve-2024-postgres-auth-bypass",
        "rawcontent": "Una vulnerabilidad de evasión de autenticación afecta a PostgreSQL 15.x y 11.x bajo conexiones TLS específicas. Permite a usuarios no autenticados conectarse como superusuario.",
        "tags": {
            "cve_id": "CVE-2024-PG-5590",
            "severidad": "Crítico",
            "activos_afectados": {"postgresql": ["15.x", "11.x"]},
            "acción_recomendada": "Deshabilitar TLS temporalmente o actualizar a las versiones menores correctivas.",
            "puntuacion_cvss": "9.0",
            "tipo_vulnerabilidad": "Authentication Bypass",
            "estado_vulnerabilidad": "Parche Disponible"
        }
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
