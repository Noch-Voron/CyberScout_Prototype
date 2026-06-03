from google import genai
import os
import json
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

async def clasificar_noticias(article: str):

    prompt = f"""
    You are an experienced cybersecurity analyst.

    Analyze the following cybersecurity news article and extract structured information.
    
    The article may be about many different topics, including:
    
    * Vulnerabilities
    * Malware
    * Data breaches
    * Threat reports
    * Security research
    * Best practices
    * Webinars or conferences
    * Product or tool announcements
    * Other cybersecurity-related topics
    
    First determine the category of the article.
    
    Valid categories:
    
    * VULNERABILITY
    * MALWARE
    * DATA_BREACH
    * THREAT_REPORT
    * SECURITY_RESEARCH
    * BEST_PRACTICES
    * WEBINAR
    * TOOL_RELEASE
    * OTHER
    
    Return ONLY a valid JSON object with the following schema:
    
    {
    "categoria": "string",
    "cve_id": "string | null",
    "severidad": "critico | alto | medio | bajo | null",
    "activos_afectados": {
    "product_name": ["version1", "version2"]
    },
    "accion_recomendada": "string",
    "puntuacion_cvss": "string | null",
    "tipo_vulnerabilidad": "string | null",
    "estado_vulnerabilidad": "string | null"
    }
    
    Rules:
    
    1. Return ONLY valid JSON.
    2. Do NOT include markdown.
    3. Do NOT include explanations.
    4. Do NOT include text before or after the JSON.
    5. Use null when information cannot be determined from the article.
    6. Do not invent CVEs, CVSS scores, versions, products, patches, or vulnerability types.
    7. activos_afectados must be an empty object {} if no affected assets are identified.
    8. accion_recomendada should be empty string "" if no recommendation can be inferred.
    
    Special rules for non-vulnerability articles:
    
    If categoria is NOT "VULNERABILITY", then:
    
    * cve_id = null
    * puntuacion_cvss = null
    * tipo_vulnerabilidad = null
    * estado_vulnerabilidad = null
    * severidad = null
    
    Severity mapping:
    
    * critico
    * alto
    * medio
    * bajo
    
    Only assign severity when the article describes an actual vulnerability, exploit, malware campaign, or security incident with a meaningful impact level.
    
    Article:
    
    {article}

    """
    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(respuesta.text)
