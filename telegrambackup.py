# services/telegram_alert.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

load_dotenv()

# Get the bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the bot globally
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_telegram_message(message: str):
    """
    Sends a message to the most recent chat that messaged the bot.
    This requires you to have already sent a /start message to the bot at least once.
    """
    try:
        updates = await bot.get_updates()
        if not updates:
            logger.error("No recent messages found to determine chat_id.")
            return

        chat_id = updates[-1].message.chat.id
        await bot.send_message(
            chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Message sent successfully.")

    except Exception as e:
        logger.error(f"Telegram error: {e}")


def send_pipeline_status(status: str, symbol: str):
    message = f"\n*Pipeline {status}* for `{symbol}`"
    asyncio.run(send_telegram_message(message))


def send_trade_alert(symbol: str, action: str, price: float, date: str):
    message = f"\n*ALERT: {action} Signal*\nSymbol: `{symbol}`\nPrice: `{price}`\nDate: `{date}`"
    asyncio.run(send_telegram_message(message))


def send_error_alert(error: str):
    message = f"\n*ERROR Occurred:*\n```{error}```"
    asyncio.run(send_telegram_message(message))
