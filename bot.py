import os
import json
from datetime import datetime, timedelta, date
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@Motobrat_news")
EVENTS_FILE = "events_2026.json"
REMINDER_DAYS = 5

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN ist nicht gesetzt")


def load_events():
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def is_reminder_day(event_date):
    return event_date - timedelta(days=REMINDER_DAYS) == date.today()


def send_event(bot, event, event_date):
    title = event.get("title", "Event")
    description = event.get("description", "")
    image = event.get("image")

    caption = (
        f"📅 *{title}*\n"
        f"🗓 *{event_date.strftime('%d.%m.%Y')}*\n\n"
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


def main():
    bot = Bot(token=BOT_TOKEN)
    events = load_events()
    today = date.today()

    for event in events:

        # 🔹 EINZELTERMIN
        if "start_date" in event:
            event_date = parse_date(event["start_date"])

            if is_reminder_day(event_date):
                send_event(bot, event, event_date)

        # 🔹 SERIENTERMIN
        elif "recurring" in event:
            recurring = event["recurring"]
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

            start = parse_date(recurring["start"])
            end = parse_date(recurring["end"])
            rule = recurring["rule"]
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt")
    if not chat_id:
        raise RuntimeError("TELEGRAM_CHAT_ID fehlt")

            current = start
            while current <= end:
    bot = Bot(token=token)

                if rule == "first_sunday" and current.weekday() == 6 and current.day <= 7:
                    if is_reminder_day(current):
                        send_event(bot, event, current)

                if rule == "third_saturday" and current.weekday() == 5 and 15 <= current.day <= 21:
                    if is_reminder_day(current):
                        send_event(bot, event, current)

                current += timedelta(days=1)

        else:
            print(f"⚠️ Ungültiges Event übersprungen: {event}")
    bot.send_message(
        chat_id=chat_id,
        text="✅ TEST OK – GitHub Actions → Telegram funktioniert!"
    )

    print("Telegram Nachricht erfolgreich gesendet")

if __name__ == "__main__":
