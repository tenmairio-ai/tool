import os
import threading

from flask import Flask
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("8985526419:AAHkT58JguHBo2dUNQM5t-7LkvlzcqDGcDw")

if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN environment variable")

# =========================
# RENDER WEB SERVER
# =========================

app = Flask(__name__)


@app.route("/")
def home():
    return "TXGAME MD5 BOT - ONLINE", 200


@app.route("/health")
def health():
    return "OK", 200


# =========================
# TELEGRAM BOT
# =========================

WELCOME = """⚡️ TXGAME MD5 ⚡️

━━━━━━━━━━━━━━━━━━━━

❗️ Tool được tạo bởi @lionVnIos

🔬 Phân tích MD5 / SHA-256

━━━━━━━━━━━━━━━━━━━━

❗️ Cách sử dụng ❗️

👉🏽 Dán mã MD5 hoặc mã SHA-256 vào đây
"""


async def start(update, context):
    await update.message.reply_text(WELCOME)


async def handle_hash(update, context):

    value = update.message.text.strip()

    # Chỉ nhận MD5 hoặc SHA-256
    if len(value) == 32:
        hash_type = "MD5"

    elif len(value) == 64:
        hash_type = "SHA-256"

    else:
        await update.message.reply_text(
            "❌ Mã không hợp lệ."
        )
        return

    # Phân tích thống kê đơn giản
    unique = len(set(value))

    score = min(
        100,
        (unique / 16) * 100
    )

    result = (
        "⚡️ TXGAME MD5\n"
        f"🔐 Kết quả: {hash_type}\n"
        f"📊 Điểm phân tích: {score:.1f}%"
    )

    await update.message.reply_text(result)


# =========================
# CHẠY TELEGRAM
# =========================

def run_bot():

    telegram_app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    telegram_app.add_handler(
        CommandHandler("start", start)
    )

    telegram_app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_hash
        )
    )

    telegram_app.run_polling()


# =========================
# START
# =========================

if __name__ == "__main__":

    bot_thread = threading.Thread(
        target=run_bot,
        daemon=True
    )

    bot_thread.start()

    port = int(os.getenv("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
