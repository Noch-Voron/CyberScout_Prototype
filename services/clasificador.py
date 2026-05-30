from google import genai
import os
import json
# poner key real XD
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

async def clasificar_noticias(article: str):

    prompt = f"""
    You are a cybersecurity analyst.
    
    Analyze the following cybersecurity news article.
    
    Return ONLY valid JSON matching exactly this schema:
    
    {{
      "cve_id": "string or null",
      "severidad": "critico|alto|medio|bajo",
      "activos_afectados": {{
        "Product Name": ["version1", "version2"]
      }},
      "accion_recomendada": "string",
      "puntuacion_cvss": "string or null",
      "tipo_vulnerabilidad": "string or null",
      "estado_vulnerabilidad": "string"
    }}
    
    Field descriptions:
    
    - cve_id: CVE identifier if mentioned, otherwise null.
    - severidad: one of critico, alto, medio, bajo.
    - activos_afectados: dictionary where keys are affected products/assets and values are lists of affected versions.
    - accion_recomendada: recommended mitigation or action. Empty string if none.
    - puntuacion_cvss: CVSS score if mentioned, otherwise null.
    - tipo_vulnerabilidad: vulnerability type such as RCE, XSS, SQL Injection, Privilege Escalation, etc. Null if unknown.
    - estado_vulnerabilidad: status such as "sin parche", "con parche", "mitigado", "desconocido".
    
    Article:
    
    {article}
    
    Return ONLY the JSON object.
    """
    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(respuesta.text)
