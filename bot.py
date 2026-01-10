import json
import os
import requests
import datetime

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@Motobrat_news"

def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHANNEL, "text": text})

today = datetime.date.today()

with open("events_2026.json", encoding="utf-8") as f:
    events = json.load(f)

for e in events:
    event_date = datetime.date.fromisoformat(e["date"])

    if event_date == today:
        send(f"📅 Neuer Termin\n\n{e['title']} am {e['date']}")

    if event_date - today == datetime.timedelta(days=1):
        send(f"⏰ Erinnerung – morgen!\n\n{e['title']} am {e['date']}")
