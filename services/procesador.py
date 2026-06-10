import json
import asyncio
from db.database import db
from services.clasificador import clasificar_noticias
from services.notificador import notificador
from motor_de_cruce.motor import evaluar_noticia, Inventario_Local
from motor_de_cruce.models import noticiaEstructurada  

async def procesar_noticias():
    if not db.pool:
        return

    try:
        async with db.pool.acquire() as conn:
            noticias_pendientes = await conn.fetch("""
                SELECT id, title, url, rawcontent 
                FROM noticias 
                WHERE processed = FALSE
            """)

            if not noticias_pendientes:
                return 

            print(f"Encontradas {len(noticias_pendientes)} noticias pendientes. Enviando a Gemini...")

            for noticia in noticias_pendientes:
                noticia_id = noticia["id"]
                texto_crudo = noticia["rawcontent"]
                
                try:
                    # 1. Llamamos a Gemini
                    resultado_json = await clasificar_noticias(texto_crudo)
                    tags_json_str = json.dumps(resultado_json)

                    # ---> LA ADUANA DE CRISTÓBAL EMPIEZA AQUÍ <---
                    
                    # 2. Convertimos el JSON de Gemini al modelo Pydantic del motor
                    noticia_obj = noticiaEstructurada(**resultado_json)
                    
                    # 3. Pasamos la noticia por el Motor de Cruce
                    alertas_generadas = evaluar_noticia(noticia_obj, Inventario_Local)

                    # ---> LA ADUANA DE CRISTÓBAL TERMINA AQUÍ <---

                    # 4. Guardamos la noticia en la Base de Datos como procesada
                    await conn.execute("""
                        UPDATE noticias 
                        SET processed = TRUE, 
                            tags = $1, 
                            processdate = NOW()
                        WHERE id = $2
                    """, tags_json_str, noticia_id)
                    
                    print(f"Noticia ID {noticia_id} clasificada y guardada.")
                    
                    # 5. El Filtro: Solo notificamos al Frontend si hay servidores en peligro
                    if alertas_generadas:
                        print(f"⚠️ ¡PELIGRO! Se detectaron {len(alertas_generadas)} servidores afectados. Notificando al SOC...")
                        
                        alerta_realtime = {
                            "id": noticia_id,
                            "title": noticia["title"],
                            "url": noticia["url"],
                            "tags": resultado_json, 
                            "processdate": "Justo ahora", 
                            "alerta_nueva": True,
                            # Extraemos los nombres de los servidores afectados de la lista de alertas
                            "servidores_afectados": [alerta.nombre_servidor for alerta in alertas_generadas]
                        }
                        
                        # Disparamos la alerta al Frontend (React)
                        await notificador.notificar_nueva_alerta(alerta_realtime)
                    else:
                        print(f"✅ La amenaza ID {noticia_id} no afecta a nuestra infraestructura. Descartada por el Motor.")
                    
                except Exception as e:
                    print(f" Error procesando la noticia ID {noticia_id}: {e}")
                
                # Respetar el límite de solicitudes de la API de Gemini (ej. 15s - 20s de espera)
                await asyncio.sleep(15)
                    
    except Exception as e:
        print(f" Error fatal en el loop del procesador: {e}")