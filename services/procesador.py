import json
from db.database import db
from services.clasificador import clasificar_noticias
from services.notificador import notificador  

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
                    
                    resultado_json = await clasificar_noticias(texto_crudo)
                    
                    
                    tags_json_str = json.dumps(resultado_json)

                    
                    await conn.execute("""
                        UPDATE noticias 
                        SET processed = TRUE, 
                            tags = $1, 
                            processdate = NOW()
                        WHERE id = $2
                    """, tags_json_str, noticia_id)
                    
                    print(f"Noticia ID {noticia_id} clasificada y guardada.")
                    alerta_realtime = {
                        "id": noticia_id,
                        "title": noticia["title"],
                        "url": noticia["url"],
                        "tags": resultado_json, 
                        "processdate": "Justo ahora", 
                        "alerta_nueva": True
                    }
                    
                    
                    await notificador.notificar_nueva_alerta(alerta_realtime)
                    
                except Exception as e:
                    print(f" Error procesando la noticia ID {noticia_id}: {e}")
                    
    except Exception as e:
        print(f" Error fatal en el loop del procesador: {e}")