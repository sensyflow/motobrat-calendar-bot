import json
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN ist nicht gesetzt")

EVENTS_FILE = "events/events_2026.json"


def load_events():
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def format_event(event):
    date = datetime.date.fromisoformat(event["date"]).strftime("%d.%m.%Y")
    text = (
        f"📅 {date}\n"
        f"📍 {event['location']}\n\n"
        f"🔥 {event['title']}\n"
        f"{event['description']}\n\n"
        "🏍️ MOTOBRAT MC"
    )
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏍️ Willkommen beim MOTOBRAT MC Kalender Bot!\n\n"
        "Befehle:\n"
        "/next – nächster Termin\n"
        "/month – Termine diesen Monat"
    )


async def next_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    events = load_events()

    future_events = [
        e for e in events
        if datetime.date.fromisoformat(e["date"]) >= today
    ]

    if not future_events:
        await update.message.reply_text("Keine kommenden Termine.")
        return

    next_e = sorted(future_events, key=lambda e: e["date"])[0]
    await update.message.reply_text(format_event(next_e))


async def month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    events = load_events()

    month_events = [
        e for e in events
        if datetime.date.fromisoformat(e["date"]).month == today.month
        and datetime.date.fromisoformat(e["date"]).year == today.year
    ]

    if not month_events:
        await update.message.reply_text("Keine Termine diesen Monat.")
        return

    text = "📅 Termine diesen Monat:\n\n"
    for e in sorted(month_events, key=lambda e: e["date"]):
        d = datetime.date.fromisoformat(e["date"]).strftime("%d.%m.")
        text += f"• {d} – {e['title']}\n"

    await update.message.reply_text(text)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", next_event))
    app.add_handler(CommandHandler("month", month))

    app.run_polling()


if __name__ == "__main__":
    main()

