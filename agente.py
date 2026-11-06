import os
import requests

bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

print("Preguntando a Google qué modelos tienes disponibles...")
url_modelos = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_api_key}"
respuesta = requests.get(url_modelos)

if respuesta.status_code == 200:
    datos = respuesta.json()
    # Extraemos los nombres de los modelos compatibles con texto
    modelos_texto = [m['name'] for m in datos.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
    lista = "\n".join(modelos_texto)
    mensaje_final = f"✅ **Modelos autorizados en tu cuenta:**\n\n{lista}"
else:
    mensaje_final = f"⚠️ Error {respuesta.status_code} al verificar la clave."

print("Enviando lista a Telegram...")
requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": mensaje_final[:4000]})
print("Fin de la comprobación.")
