import os
import requests

bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

prompt = """
Actúa como experto en ventas B2B químicas.
Busca 3 fábricas o empresas (en España o Europa) que necesiten COMPRAR materias primas como ceras de polietileno, resinas PP/PE o pigmentos (ej: fabricantes de masterbatch, plásticos, adhesivos).
Para cada empresa detalla:
- Nombre
- Sector/Qué fabrican
- País y web
Dame solo la lista.
"""

url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
data = {"contents": [{"parts": [{"text": prompt}]}]}

print("Consultando a Gemini...")
respuesta_gemini = requests.post(url_gemini, json=data)

# AQUÍ ESTÁ EL TRUCO: Si Google falla, imprimimos su mensaje secreto
if respuesta_gemini.status_code == 200:
    datos = respuesta_gemini.json()
    leads = datos['candidates'][0]['content']['parts'][0]['text']
    mensaje_final = f"🎯 **Nuevos Clientes (Compradores):**\n\n{leads}"
    print("IA completada con éxito.")
else:
    print(f"🛑 CÓDIGO DE ERROR DE GOOGLE: {respuesta_gemini.status_code}")
    print(f"🛑 DETALLE DEL ERROR: {respuesta_gemini.text}")
    mensaje_final = f"⚠️ Fallo en Gemini. Revisa la consola de GitHub."

print("Enviando a Telegram...")
requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": mensaje_final})
print("Fin del proceso.")
