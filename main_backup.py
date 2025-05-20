from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
# app.secret_key = "4f8d6c5372bce38a65f741a23854eb36b697efcfe5dfc275e0f7a764a2eae01e"
CORS(app)  # Cho phép frontend gọi API (nếu khác domain)


def read_data_file():
    with open("thong_tin_nganh.txt", "r", encoding="utf-8") as f:
        return f.read()


client = OpenAI(
    api_key="sk-64ec86526ab74f68948e90be4c612351",  # Hoặc lấy từ biến môi trường
    base_url="https://api.deepseek.com"  # DeepSeek
)

# @app.route("/set_thong_tin_user", methods=["POST"])
# def set_profile():
#     data = request.get_json()
#     session['profile'] = {
#         "name": data.get("name"),
#         "email": data.get("email")
#     }
#     return jsonify({"message": "Profile saved in session"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    # Đọc nội dung file data.txt
    file_data = read_data_file()
    # print("Session hiện tại:", dict(session))
    # # Lấy profile từ session
    # profile = session.get("profile", {})
    # name = profile.get("name", "Người dùng")
    # email = profile.get("email", "email")

    # # Ví dụ dùng name + sở thích để cá nhân hoá prompt
    # personal_info = f"Tên của người dùng là {name}. " \
    #                 f"Email: {email}."

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages = [
            {"role": "system", "content": f"Dưới đây là dữ liệu tham khảo:\n{file_data}"},
            # {"role": "system", "content": f"Thông tin người dùng: \n{personal_info}"},
            {"role": "user", "content": user_message}
        ]
    )

    bot_message = response.choices[0].message.content
    return jsonify({"reply": bot_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))