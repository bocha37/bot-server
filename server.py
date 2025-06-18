from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === Переменные окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# === Обработка вопроса от пользователя ===
@app.route('/question', methods=['POST'])
def handle_question():
    data = request.json
    question = data.get('question')
    user_id = data.get('user_id') or 'Неизвестный'

    if not question:
        return jsonify({"error": "Вопрос не может быть пустым"}), 400

    # Отправляем вопрос админу
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" 
    text = f"📩 Вопрос от пользователя {user_id}:\n\n{question}"

    try:
        response = requests.post(url, json={"chat_id": ADMIN_ID, "text": text})
        return jsonify({"status": "ok", "response": response.json()})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

# === Ответ админа через Telegram ===
@app.route('/answer', methods=['POST'])
def answer_to_user():
    data = request.json
    user_id = data.get('user_id')
    answer_text = data.get('answer')

    if not user_id or not answer_text:
        return jsonify({"error": "Нет данных для отправки"}), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" 
    payload = {
        "chat_id": user_id,
        "text": f"💬 Ответ от эксперта:\n{answer_text}"
    }

    try:
        response = requests.post(url, json=payload)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})