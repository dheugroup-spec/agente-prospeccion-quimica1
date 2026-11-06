import os
import requests
import json

# Cargar credenciales y LIMPIAR espacios en blanco invisibles automáticamente (.strip())
bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

# Instrucciones para la IA: Búsqueda de CLIENTES POTENCIALES
prompt = """
Actúa como un experto en desarrollo de negocio B2B y ventas del sector químico.
Tu objetivo es buscar CLIENTES POTENCIALES (fabricantes industriales) que necesiten COMPRAR materias primas como:
- Ceras de Polietileno (PE) y Polipropileno (PP)
- Resinas de PE y PP
- Pigmentos (como Dióxido de Titanio)

Busca 3 empresas reales (en España o Europa) que utilicen habitualmente estos productos químicos en sus procesos de fabricación (por ejemplo: fabricantes de masterbatch, plásticos, adhesivos hot melt, tintas, pinturas, recubrimientos o PVC).

Para cada empresa compradora, detalla brevemente:
- Nombre de la empresa
- Sector o qué fabrican (para qué usan estas materias primas exactas)
- País y página web

No incluyas introducciones, dame directamente la lista estructurada.
"""

# Pedir a Gemini que busque los leads
url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"
headers = {'Content-Type': 'application/json'}
data = {"contents": [{"parts": [{"text": prompt}]}]}

print("Buscando clientes potenciales...")
try:
    respuesta_gemini = requests.post(url_gemini, headers=headers, data=json.dumps(data))
    respuesta_gemini.raise_for_status()
    datos = respuesta_gemini.json()
    leads = datos['candidates'][0]['content']['parts'][0]['text']
    mensaje_final = f"🎯 **Nuevos Posibles Clientes (Compradores):**\n\n{leads}"
except Exception as e:
    print(f"Error al consultar a la IA: {e}")
    mensaje_final = "⚠️ Hubo un error al generar los clientes, revisa los registros en GitHub."

# Enviar los resultados a Telegram
print("Enviando reporte a Telegram...")
url_telegram = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": mensaje_final,
    "parse_mode": "Markdown"
}

try:
    respuesta_telegram = requests.post(url_telegram, json=payload)
    respuesta_telegram.raise_for_status()
    print("¡Reporte enviado con éxito!")
except Exception as e:
    print(f"Error al enviar a Telegram: {e}")
