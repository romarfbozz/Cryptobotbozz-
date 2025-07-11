import os
import time
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TRADINGVIEW_URL = "https://www.tradingview.com/ideas/btc/"

seen_ideas = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=payload)
        if not r.ok:
            print(f"Ошибка Telegram API: {r.status_code} — {r.text}")
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")

def parse_tradingview_ideas():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        resp = requests.get(TRADINGVIEW_URL, headers=headers)
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
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return []

def send_new_ideas():
    global seen_ideas
    ideas = parse_tradingview_ideas()
    new_count = 0

    for idea in ideas:
        if idea["link"] not in seen_ideas:
            message = f"📈 <b>{idea['title']}</b>\n{idea['link']}"
            send_telegram_message(message)
            print(f"Отправлено: {idea['title']}")
            seen_ideas.add(idea["link"])
            new_count += 1

    if new_count == 0:
        print("Новых идей нет.")

if __name__ == "__main__":
    print("✅ Бот запущен (через requests)")
    while True:
        send_new_ideas()
        time.sleep(300)  # каждые 5 минут
