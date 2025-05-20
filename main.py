from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Hoặc dùng một chuỗi bí mật cố định
CORS(app, supports_credentials=True)  # Cho phép dùng session từ frontend

user_chat_histories = {}

def read_data_file():
    with open("thong_tin_nganh.txt", "r", encoding="utf-8") as f:
        return f.read()


client = OpenAI(
    api_key="sk-64ec86526ab74f68948e90be4c612351",  # Hoặc lấy từ biến môi trường
    base_url="https://api.deepseek.com"  # DeepSeek
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    user_name = data.get("name")    # Lấy thêm name
    user_email = data.get("email")  # Lấy thêm email
    personal_info = f"Tên: {user_name}\nEmail: {user_email}" if user_name and user_email else "Không có thông tin người dùng"


    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    file_data = read_data_file()

    history = user_chat_histories.get(user_email, [])

if not history:
    history = []
    history.append({"role": "system", "content": f"Dưới đây là dữ liệu tham khảo:\n{file_data}"})
    history.append({"role": "system", "content": f"Thông tin người dùng:\n{personal_info}"})

# Sau đó mới cắt:
MAX_HISTORY_LENGTH = 20
base_messages = history[:2]  # giữ lại 2 dòng đầu: dữ liệu + info người dùng
chat_messages = history[2:]

if len(chat_messages) > MAX_HISTORY_LENGTH:
    chat_messages = chat_messages[-MAX_HISTORY_LENGTH:]

history = base_messages + chat_messages

    # Thêm câu hỏi người dùng
    history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history
    )

    bot_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": bot_message})
    # Lưu lại
    user_chat_histories[user_email] = history
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))