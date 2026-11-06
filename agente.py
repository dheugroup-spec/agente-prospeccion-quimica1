import os
import requests
import time

bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

prompt = """
Actúa como un experto en desarrollo de negocio B2B y ventas del sector químico.
Busca 3 empresas reales (en España o Europa) que necesiten COMPRAR materias primas como:
- Ceras de Polietileno (PE) y Polipropileno (PP)
- Resinas de PE y PP
- Pigmentos (como Dióxido de Titanio)
Para cada empresa compradora, detalla brevemente: nombre, sector/qué fabrican, y país/web. Dame solo la lista estructurada.
"""

# Lista de modelos por orden de preferencia para evitar saturaciones
modelos_a_probar = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-2.5-flash"]
leads = None

data = {"contents": [{"parts": [{"text": prompt}]}]}

for modelo in modelos_a_probar:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={gemini_api_key}"
    try:
        resp = requests.post(url, json=data, timeout=15)
        if resp.status_code == 200:
            datos = resp.json()
            leads = datos['candidates'][0]['content']['parts'][0]['text']
            break
        elif resp.status_code == 503:
            print(f"Modelo {modelo} saturado (503), probando siguiente...")
            time.sleep(2)
    except Exception as e:
        print(f"Error con {modelo}: {e}")

if leads:
    mensaje_final = f"🎯 **Nuevos Clientes (Químico):**\n\n{leads}"
else:
    mensaje_final = "⚠️ El servicio de Google está temporalmente saturado en este momento. Se reintentará mañana automáticamente."

requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": mensaje_final})
