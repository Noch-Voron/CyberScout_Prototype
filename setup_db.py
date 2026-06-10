import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def run():
    dsn = os.getenv("dsn")
    if not dsn:
        print("Error: No se encontró la variable 'dsn' en el archivo .env")
        return
        
    print(f"Conectando a la base de datos...")
    try:
        conn = await asyncpg.connect(dsn)
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return
    
    # Crear la tabla noticias
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS public.noticias (
                id serial PRIMARY KEY,
                url text UNIQUE NOT NULL,
                title text,
                rawcontent text,
                extractdate timestamp DEFAULT CURRENT_TIMESTAMP,
                processdate timestamp,
                processed boolean DEFAULT false,
                tags json
            );
        """)
        print("Tabla public.noticias creada exitosamente (o ya existía).")
    except Exception as e:
        print(f"Error creando la tabla noticias: {e}")
        await conn.close()
        return

    # Crear la tabla fuentes
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS public.fuentes (
                id serial PRIMARY KEY,
                url text UNIQUE NOT NULL,
                processdate timestamp,
                processed boolean DEFAULT false
            );
        """)
        print("Tabla public.fuentes creada exitosamente (o ya existía).")
    except Exception as e:
        print(f"Error creando la tabla fuentes: {e}")
        await conn.close()
        return
    
    # Intentar asignar dueño y permisos
    for tabla in ["noticias", "fuentes"]:
        try:
            await conn.execute(f"ALTER TABLE public.{tabla} OWNER TO cyberscout;")
            print(f"Propietario de la tabla '{tabla}' cambiado a 'cyberscout'.")
        except Exception as e:
            print(f"Nota: No se pudo cambiar el propietario de '{tabla}' a 'cyberscout' (es posible que el rol no exista localmente): {e}")
            
        try:
            await conn.execute(f"GRANT ALL ON TABLE public.{tabla} TO cyberscout;")
            print(f"Permisos de '{tabla}' concedidos a 'cyberscout'.")
        except Exception as e:
            print(f"Nota: No se pudieron conceder los permisos de '{tabla}' a 'cyberscout': {e}")
        
    await conn.close()
    print("Proceso finalizado.")

if __name__ == "__main__":
    asyncio.run(run())
