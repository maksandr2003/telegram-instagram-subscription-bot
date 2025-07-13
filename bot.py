import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import aiohttp

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("TELEGRAM_CHANNEL_USERNAME")
PDF_LINK = os.getenv("PDF_LINK")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Перейти в Instagram", url="https://www.instagram.com/astrolog.chemerys")],
        [InlineKeyboardButton("Я подписался на Instagram", callback_data="subscribed_instagram")]
    ]
    await update.message.reply_text(
        "Чтобы получить бесплатную книгу, подпишитесь на Instagram и Telegram.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "subscribed_instagram":
        keyboard = [
            [InlineKeyboardButton("Перейти в Telegram канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("Я подписан на Telegram", callback_data="check_telegram")]
        ]
        await query.edit_message_text(
            "Теперь подпишитесь на Telegram-канал:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "check_telegram":
        user_id = query.from_user.id
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}"
            async with session.get(url) as resp:
                data = await resp.json()

        if data.get("ok") and data["result"]["status"] in ["member", "creator", "administrator"]:
            await query.edit_message_text(
                f"✅ Спасибо за подписку! Вот ссылка на PDF: {PDF_LINK}"
            )
        else:
            keyboard = [
                [InlineKeyboardButton("Перейти в Telegram канал", url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton("Я подписан на Telegram", callback_data="check_telegram")]
        ]
            await query.edit_message_text(
                "❗️Похоже, вы ещё не подписаны на канал. Пожалуйста, подпишитесь и нажмите кнопку ещё раз.", 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    from flask import Flask
    import threading

    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Bot is running!', 200

    def run_flask():
        app.run(host='0.0.0.0', port=10000)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    threading.Thread(target=run_flask).start()
    app.run_polling()
