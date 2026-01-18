import os
from telegram import Bot

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt")
    if not chat_id:
        raise RuntimeError("TELEGRAM_CHAT_ID fehlt")

    bot = Bot(token=token)

    bot.send_message(
        chat_id=chat_id,
        text="✅ TEST OK – GitHub Actions → Telegram funktioniert!"
    )

    print("Telegram Nachricht erfolgreich gesendet")

if __name__ == "__main__":
    main()
