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

    Analyze this article and return ONLY valid JSON.

    {{
        "severity": "LOW|MEDIUM|HIGH|CRITICAL",
        "summary": "short summary",
        "affected_products": [],
        "cves": []
    }}

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
