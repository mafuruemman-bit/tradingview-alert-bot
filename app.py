from flask import Flask, request
import requests
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ==========================
# CONFIGURATION
# ==========================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")

# ==========================
# TELEGRAM FUNCTION
# ==========================
def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Missing Telegram credentials.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

# ==========================
# EMAIL FUNCTION
# ==========================
def send_email_alert(subject, body):
    if not EMAIL_USER or not EMAIL_PASS or not TO_EMAIL:
        print("⚠️ Missing email credentials.")
        return
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email send failed: {e}")

# ==========================
# MAIN WEBHOOK ENDPOINT
# ==========================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = f"📈 TradingView Alert:\n{data}"
    send_telegram_message(message)
    send_email_alert("TradingView Alert", str(data))
    return {"status": "success"}

# ==========================
# TEST ENDPOINT
# ==========================
@app.route('/send-test')
def send_test():
    try:
        message = "✅ Test alert received successfully!"
        send_telegram_message(message)
        send_email_alert("Test Alert", message)
        return "✅ Test sent to Telegram and Email!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==========================
# ROOT ROUTE
# ==========================
@app.route('/')
def home():
    return "🚀 TradingView Alert Bot is running!"

# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

