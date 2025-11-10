from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === CONFIGURE YOUR BOT ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "PUT_YOUR_CHAT_ID_HERE")

@app.route('/')
def home():
    return "✅ TradingView Alert Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return {"error": "No data received"}, 400

    message = f"📊 TradingView Alert:\n{data}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    requests.post(telegram_url, json=payload)
    return {"status": "sent"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
