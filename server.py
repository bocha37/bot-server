from flask import Flask, request, jsonify
import requests as req

app = Flask(__name__)

# === Эти данные будут заданы через переменные окружения ===
BOT_TOKEN = "7572534113:AAFdRB_U0KSVK0rCTYlnPgd_Z2-Ij0WXZ0k"
ADMIN_ID = "6348938205"

@app.route('/question', methods=['POST'])
def handle_question():
    data = request.json
    question_text = data.get("question")
    user_id = data.get("user_id", "неизвестный")

    if not question_text:
        return jsonify({"error": "Пустой вопрос"}), 400

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" 
        payload = {
            "chat_id": ADMIN_ID,
            "text": f"📩 Вопрос от пользователя {user_id}:\n\n{question_text}"
        }
        req.post(url, json=payload)

        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Bot Server работает!"

if __name__ == '__main__':
    app.run()