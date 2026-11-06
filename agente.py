import os
import requests

# 1. Cargar las credenciales de Telegram desde GitHub
bot_token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

# 2. Mensaje que el agente va a enviar
# (Más adelante aquí pondremos la lista real de empresas químicas que encuentre)
mensaje = "✅ ¡Prueba exitosa! El agente de Prospección Química está conectado y funcionando desde GitHub."

# 3. Configurar la conexión con Telegram
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": mensaje
}

# 4. Enviar el mensaje
print("Ejecutando agente y enviando resultados a Telegram...")
try:
    respuesta = requests.post(url, json=payload)
    respuesta.raise_for_status()
    print("¡Mensaje enviado a Telegram correctamente!")
except requests.exceptions.RequestException as e:
    print(f"Error al enviar el mensaje a Telegram: {e}")
