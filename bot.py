import os
import json
from datetime import datetime, timedelta, date
from telegram import Bot, InputFile

# =========================
# KONFIGURATION
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@motobrat_news"
EVENTS_FILE = "events_2026.json"
REMINDER_DAYS = 5

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN ist nicht gesetzt")

# =========================
# HILFSFUNKTIONEN
# =========================

def load_events():
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def is_reminder_day(event_date: date) -> bool:
    return event_date - timedelta(days=REMINDER_DAYS) == date.today()


def send_event(bot: Bot, event: dict):
    title = event["title"]
    start_date = event["start_date"]
    end_date = event.get("end_date")
    description = event.get("description", "")
    image = event.get("image")

    date_text = start_date
    if end_date:
        date_text += f" – {end_date}"

    caption = (
        f"📅 *{title}*\n"
        f"🗓 *{date_text}*\n\n"
        f"{description}"
    )

    if image and os.path.exists(image):
        with open(image, "rb") as img:
            bot.send_photo(
                chat_id=CHANNEL_USERNAME,
                photo=img,
                caption=caption,
                parse_mode="Markdown"
            )
    else:
        bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=caption,
            parse_mode="Markdown"
        )


# =========================
# MAIN
# =========================

def main():
    bot = Bot(token=BOT_TOKEN)
    events = load_events()

    today = date.today()

    for event in events:
        start = datetime.strptime(event["start_date"], "%Y-%m-%d").date()

        if is_reminder_day(start):
            send_event(bot, event)


if __name__ == "__main__":
    main()
