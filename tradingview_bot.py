import sys
print("🔥 Python version:", sys.version)
import os
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
URL = "https://www.tradingview.com/ideas/btc/"

bot = Bot(token=TELEGRAM_TOKEN)
seen_ideas = set()

def parse_tradingview_ideas():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(URL, headers=headers)
    if resp.status_code != 200:
        print(f"Ошибка доступа к TradingView: {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    ideas = []

    for a in soup.select("a.tv-widget-idea__title"):
        title = a.get_text(strip=True)
        link = "https://www.tradingview.com" + a['href']
        ideas.append({"title": title, "link": link})
    return ideas

def send_new_ideas():
    global seen_ideas
    ideas = parse_tradingview_ideas()
    new_count = 0

    for idea in ideas:
        if idea["link"] not in seen_ideas:
            message = f"📈 <b>{idea['title']}</b>\n{idea['link']}"
            try:
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
                print(f"Отправлено: {idea['title']}")
                seen_ideas.add(idea["link"])
                new_count += 1
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

    if new_count == 0:
        print("Новых идей нет.")

if __name__ == "__main__":
    print("Бот запущен.")
    while True:
        send_new_ideas()
        time.sleep(300)  # Ждем 5 минут
