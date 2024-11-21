import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from flask import Flask

# Thiết lập bot token và Flask app
BOT_TOKEN = "7924463442:AAESIxIkHi-3PLhH9Gv5SgINaXUckSWy1WM"
app = Flask(__name__)

@app.route("/")
def server_check():
    return "Server is running"


# Hàm start cho bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Job loa ngân hàng", callback_data="bank")], [InlineKeyboardButton("Job Minh Công", callback_data="minh_cong")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Chào mừng bạn đến với Tiot LAB", reply_markup=reply_markup)


# Xử lý callback từ nút nhấn
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print(query)
    if query.data == "bank":
        await query.edit_message_text(text="Bạn đã chọn Job loa ngân hàng")


# Xử lý tin nhắn bình thường
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    received_text = update.message.text
    await update.message.reply_text(f"Bạn vừa nhắn {received_text}")


# Hàm chạy bot
def run_telegram_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Thêm các handler cho bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT, button))

    # Chạy bot trong nền (asyncio)
    print("Bot đang chạy...")
    application.run_polling()


# Hàm khởi tạo Flask app và bot
def run_flask_app():
    asyncio.run(run_telegram_bot())
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run_flask_app()
