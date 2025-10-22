import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Cargar API_KEY (desde variables de entorno o archivo local)
load_dotenv("api.env")
API_KEY = os.getenv("openAPI")

if not API_KEY:
    raise ValueError("❌ No se encontró la variable openAPI. Configúrala en Render o en api.env")

# Configuración del endpoint de OpenRouter
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Historial global (en memoria)
historial = []

# Inicializar Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("mensaje", "")
    if not user_input:
        return jsonify({"respuesta": "⚠️ No escribiste ningún mensaje."})

    # Agregar mensaje del usuario al historial
    historial.append({"role": "user", "content": user_input})

    # Preparar cuerpo de la solicitud
    data = {
        "model": "gpt-4o-mini",
        "messages": historial,
        "max_tokens": 300
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=data)
        response.raise_for_status()
        respuesta = response.json()["choices"][0]["message"]["content"]

        # Guardar respuesta del asistente
        historial.append({"role": "assistant", "content": respuesta})

        return jsonify({"respuesta": respuesta})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"respuesta": "❌ Error al conectar con la API."})

if __name__ == "__main__":
    # Render usa el puerto asignado en la variable PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
