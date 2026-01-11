import json
import datetime
import os
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@motobrat_news"
EVENTS_FILE = "events/events_2026.json"

bot = Bot(token=BOT_TOKEN)

today = datetime.date.today()
delta = datetime.timedelta(days=5)

with open(EVENTS_FILE, "r", encoding="utf-8") as f:
    events = json.load(f)

for event in events:
    event_date = datetime.date.fromisoformat(event["date"])

    if event_date - today == delta:
        text = (
            "🔥 TERMIN-ERINNERUNG 🔥\n\n"
            f"📅 {event_date.strftime('%d.%m.%Y')}\n"
            f"📍 {event['location']}\n\n"
            f"🍻 {event['title']}\n"
            f"{event['description']}\n\n"
            "🏍️ MOTOBRAT MC"
        )

        image = event.get("image")

        if image:
            with open(image, "rb") as img:
                bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=img,
                    caption=text
                )
        else:
            bot.send_message(
                chat_id=CHANNEL_ID,
                text=text
            )
