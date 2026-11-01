
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message", "")

    token = os.environ.get("HF_TOKEN")

    if not token:
        return jsonify({"reply": "AI anahtarı henüz ayarlanmamış!"})

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "model": "meta-llama/Llama-3.1-8B-Instruct:fastest",
                "messages": [
                    {
                        "role": "system",
                        "content": "Sen BerkayAI adında Türkçe konuşan yardımcı bir yapay zekâsın."
                    },
                    {"role": "user", "content": message}
                ]
            },
            timeout=60
        )

        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]

        return jsonify({"reply": answer})

    except Exception:
        return jsonify({"reply": "Şu anda AI bağlantısı kurulamadı. Lütfen tekrar dene."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

