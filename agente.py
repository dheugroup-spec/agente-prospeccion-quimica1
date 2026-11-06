import os
import requests

bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

prompt = """
Actúa como experto en ventas B2B químicas.
Busca 3 fábricas o empresas reales (en España o Europa) que necesiten COMPRAR materias primas como ceras de polietileno, resinas PP/PE o pigmentos (ej: fabricantes de masterbatch, plásticos, adhesivos, tintas).
Para cada empresa detalla:
- Nombre de la empresa
- Sector / Qué fabrican
- País y página web
Dame directamente la lista, sin introducciones.
"""

# Hemos cambiado el modelo a "gemini-1.5-flash-latest" para asegurar compatibilidad
url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"
data = {"contents": [{"parts": [{"text": prompt}]}]}

print("Consultando a Gemini...")
respuesta_gemini = requests.post(url_gemini, json=data)

if respuesta_gemini.status_code == 200:
    datos = respuesta_gemini.json()
    leads = datos['candidates'][0]['content']['parts'][0]['text']
    mensaje_final = f"🎯 **Nuevos Clientes (Compradores):**\n\n{leads}"
    print("IA completada con éxito.")
else:
    # Si falla, probamos con el modelo clásico de reserva (gemini-pro)
    url_reserva = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}"
    respuesta_reserva = requests.post(url_reserva, json=data)
    if respuesta_reserva.status_code == 200:
        datos = respuesta_reserva.json()
        leads = datos['candidates'][0]['content']['parts'][0]['text']
        mensaje_final = f"🎯 **Nuevos Clientes (Reserva):**\n\n{leads}"
    else:
        mensaje_final = f"⚠️ Fallo definitivo en la IA. Código: {respuesta_reserva.status_code}"

print("Enviando a Telegram...")
requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": mensaje_final})
print("Fin del proceso.")
