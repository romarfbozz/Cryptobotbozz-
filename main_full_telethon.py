import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telethon.sync import TelegramClient

# Загрузка переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
USER_ID = int(os.environ.get("USER_ID"))
APP_API_ID = int(os.environ.get("APP_API_ID"))
APP_API_HASH = os.environ.get("APP_API_HASH")

# TelegramClient для Telethon
client = TelegramClient('anon', APP_API_ID, APP_API_HASH)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Я крипто-ассистент. Напиши имя монеты, например: solana")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    await update.message.reply_text(f"🔍 Сканирую Telegram по запросу: {user_input}")

    try:
        await client.start()
        dialogs = await client.get_dialogs()
        count = len(dialogs)
        await update.message.reply_text(f"✅ Найдено {count} диалогов. (Эмуляция анализа)")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при подключении к Telegram: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()
