from models import noticiaEstructurada, activoServidor, alertaGenerada
from packaging.version import parse
from packaging.specifiers import SpecifierSet
from typing import List
from time import sleep

# por ahora un inventario simple hardcodeado
Inventario_Local = [
    activoServidor(
        nombre="SRV-PROD-FEDORA",
        id="srv-001",
        entorno="Linux Fedora 42 (goated)",
        software_instalado={
            "nginx": "1.18.0",
            "python": "3.10.4",
            "postgresql": "15.2.0"
        }
    ),
    activoServidor(
        nombre="SRV-LEGACY-WIN",
        id="srv-002",
        entorno="Windows Server 2019 (trash)",
        software_instalado={
            "apache": "2.4.49",
            "java": "1.8.0",
            "postgresql": "11.5.0"
        }
    )
]

def check_version(server_version: str, threat_versions: list[str]) -> bool:
    version_obj = parse(server_version)

    for threat_v in threat_versions:
        threat_v = threat_v.strip() #take all of it's clothes off

        # caso si la noticia es tipo 4.x o 4.*, es decir no exacta
        if 'x' in threat_v.lower() or '*' in threat_v:
            clean_version = threat_v.lower().replace('x','*')
            if not clean_version.startswith("=="):
                clean_version = f"=={clean_version}"

            rule = SpecifierSet(clean_version)
            if version_obj in rule:
                return True # es match, es decir si la versión de la amenaza es 4.* y nosotros tenemos instalado 4.1.7 por ejemplo, retornará verdadero

        # caso si tenemos un <, > o si es exacto.
        else: 
            try: # si es num exacto, le ponemos un "=="
                if not any(op in threat_v for op in ["<", ">", "=", "~", "^"]):
                    rule = SpecifierSet(f"=={threat_v}")
                else: 
                    rule = SpecifierSet(threat_v)
                if version_obj in rule:
                    return True


            except Exception as e:
                print(f"Error parseando regla de versión '{threat_v}': {e}")
                continue
    return False #no hay versión exacta que afecte al cliente.
    

def evaluar_noticia(noticia: noticiaEstructurada, inventario_cliente: List[activoServidor]) -> List:
    alertas_generadas = []

    for server in inventario_cliente:
        for nombre_vuln, versiones_vuln in noticia.activos_afectados.items():
            
            match = "none" # puede ser "partial" o "full"

            if nombre_vuln in server.software_instalado:

                version = server.software_instalado[nombre_vuln]
                match = "partial" #software es afectado, aún no se determina si la versión es la misma
                if check_version(version, versiones_vuln):
                    match = "full" # versión es afectada, bad.
                
                nueva_alerta = alertaGenerada(
                    id_servidor=server.id,
                    nombre_servidor=server.nombre,
                    software_afectado=nombre_vuln,
                    nivel_match=match,
                    noticia_original=noticia
                )

                alertas_generadas.append(nueva_alerta)

    return alertas_generadas


# Benchmark (simplificado) creado por gemini, funciona como esperado.
bateria_de_noticias = [
    # TEST 1: Sin coincidencia (None)
    # Ningún servidor tiene "docker". No debería generar alerta.
    noticiaEstructurada(
        cve_id="CVE-TEST-001", severidad="Alto",
        activos_afectados={"docker": ["20.10.x"]}
    ),
    
    # TEST 2: Coincidencia Parcial (Partial)
    # El SRV-LEGACY tiene "java" (1.8.0), pero la vulnerabilidad es para versiones menores a 1.7
    noticiaEstructurada(
        cve_id="CVE-TEST-002", severidad="Medio",
        activos_afectados={"java": ["< 1.7.0"]}
    ),

    # TEST 3: Coincidencia Completa Exacta (Full)
    # El SRV-LEGACY tiene la versión exacta y prohibida de apache.
    noticiaEstructurada(
        cve_id="CVE-TEST-003", severidad="Crítico",
        activos_afectados={"apache": ["2.4.49"]}
    ),

    # TEST 4: Límites del Parser - Comodines y Rangos (Full)
    # SRV-PROD tiene python 3.10.4. Cae dentro de ">=3.8, <3.11".
    noticiaEstructurada(
        cve_id="CVE-TEST-004", severidad="Alto",
        activos_afectados={"python": [">=3.8, <3.11", "3.12.x"]}
    ),

    # TEST 5: Límites del Parser - "x" vs "*" vs Basura (Full x2)
    # Pone a prueba el reemplazo de la x. Ambos servidores tienen postgresql.
    # SRV-PROD (15.2.0) hace match con "15.x". SRV-LEGACY (11.5.0) hace match con "11.*".
    # Incluye un string basura "texto-inutil" que el motor debería ignorar sin caerse.
    noticiaEstructurada(
        cve_id="CVE-TEST-005", severidad="Crítico",
        activos_afectados={"postgresql": ["15.x", "11.*", "texto-inutil"]}
    )
]

if __name__ == "__main__":
    print("Iniciando Benchmark de CyberScout...\n")
    sleep(1)
    for i, noticia in enumerate(bateria_de_noticias, 1):
        print(f"--- Evaluando Noticia {i}: {noticia.cve_id} ---")
        sleep(1)
        resultados = evaluar_noticia(noticia, Inventario_Local)
        
        if not resultados:
            print("  Ningún servidor afectado (None).")
            sleep(1)
        
        for alerta in resultados:
            print(f"  Coincidencia {alerta.nivel_match.upper()}: {alerta.nombre_servidor} en {alerta.software_afectado}")
        print()