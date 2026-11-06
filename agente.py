import os
import requests

# 1. Cargar credenciales limpias
bot_token = os.environ.get('TELEGRAM_TOKEN', '').strip()
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '').strip()
gemini_api_key = os.environ.get('GEMINI_API_KEY', '').strip()

# 2. Instrucciones de búsqueda de COMPRADORES
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

# 3. Conectar con el modelo EXACTO de tu cuenta (gemini-2.5-flash)
url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_api_key}"
data = {"contents": [{"parts": [{"text": prompt}]}]}

print("Buscando clientes potenciales...")
respuesta_gemini = requests.post(url_gemini, json=data)

if respuesta_gemini.status_code == 200:
    datos = respuesta_gemini.json()
    leads = datos['candidates'][0]['content']['parts'][0]['text']
    mensaje_final = f"🎯 **Nuevos Posibles Clientes (Compradores):**\n\n{leads}"
    print("Búsqueda exitosa.")
else:
    mensaje_final = f"⚠️ Fallo de la IA. Código: {respuesta_gemini.status_code}\nDetalle: {respuesta_gemini.text[:200]}"
    print("Error en Gemini.")

# 4. Enviar a Telegram
print("Enviando reporte a Telegram...")
requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": mensaje_final})
print("Fin del proceso.")
