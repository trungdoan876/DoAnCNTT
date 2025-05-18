from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Cho phép frontend gọi API (nếu khác domain)

client = OpenAI(
    api_key="sk-64ec86526ab74f68948e90be4c612351",  # Hoặc lấy từ biến môi trường
    base_url="https://api.deepseek.com"  # DeepSeek
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý giúp sinh viên chọn chuyên ngành CNTT."},
            {"role": "user", "content": user_message}
        ]
    )

    bot_message = response.choices[0].message.content
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))