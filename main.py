from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

user_chat_histories = {}

def read_data_file():
    with open("thong_tin_nganh.txt", "r", encoding="utf-8") as f:
        return f.read()

client = OpenAI(
    api_key="sk-64ec86526ab74f68948e90be4c612351",
    base_url="https://api.deepseek.com"
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    user_name = data.get("name")
    user_email = data.get("email")

    personal_info = (
        f"Tên: {user_name}\nEmail: {user_email}"
        if user_name and user_email else "Không có thông tin người dùng"
    )

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    file_data = read_data_file()
    history = user_chat_histories.get(user_email, [])

    if not history:
        history = []
        history.append({
            "role": "system",
            "content": f"Dưới đây là dữ liệu tham khảo:\n{file_data}"
        })
        history.append({
            "role": "system",
            "content": f"Thông tin người dùng:\n{personal_info}"
        })

    MAX_HISTORY_LENGTH = 20
    base_messages = history[:2]
    chat_messages = history[2:]

    if len(chat_messages) > MAX_HISTORY_LENGTH:
        chat_messages = chat_messages[-MAX_HISTORY_LENGTH:]

    history = base_messages + chat_messages
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history
    )

    bot_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": bot_message})
    user_chat_histories[user_email] = history

    return jsonify({"reply": bot_message})

#new đoạn chat mới -> xóa lịch sử
@app.route("/reset", methods=["POST"])
def reset_history():
    data = request.get_json()
    user_email = data.get("email")

    if not user_email:
        return jsonify({"error": "No email provided"}), 400

    if user_email in user_chat_histories:
        del user_chat_histories[user_email]
        return jsonify({"message": "Lịch sử chat đã được đặt lại."})
    else:
        return jsonify({"message": "Không tìm thấy lịch sử chat để đặt lại."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
