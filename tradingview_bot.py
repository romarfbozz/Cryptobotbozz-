import feedparser
import time
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))
RSS_URL = os.getenv('RSS_URL')

bot = Bot(token=TELEGRAM_TOKEN)
seen_entries = set()

def fetch_and_send():
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        if entry.id not in seen_entries:
            message = f"📈 Новая идея TradingView:\n\n{entry.title}\n{entry.link}"
            bot.send_message(chat_id=CHAT_ID, text=message)
            seen_entries.add(entry.id)

if __name__ == "__main__":
    while True:
        fetch_and_send()
        time.sleep(300)
