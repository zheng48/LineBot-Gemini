from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 Flask
app = Flask(__name__)

# 設定 LINE Bot 認證
CHANNEL_ACCESS_TOKEN = ""  # 請替換成你的 token
CHANNEL_SECRET = ""  # 請替換成你的 secret

# 設定 LINE Bot API
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 設定 Gemini API
GOOGLE_API_KEY = ""  # 請替換成你的 API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 標頭的值
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        # 使用 Gemini 生成回應
        response = model.generate_content(event.message.text)
        
        # 發送回應給使用者
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=response.text)]
                )
            )
    except Exception as e:
        print(f"Error: {str(e)}")
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="抱歉，發生了一些錯誤，請稍後再試。")]
                )
            )

if __name__ == "__main__":
    # 改用 5001 端口
    port = 5001
    print(f"Flask app is running on port {port}")
    app.run(host="0.0.0.0", port=port)