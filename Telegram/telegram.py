import os
import telebot
from dotenv import load_dotenv
from vulnops.utils.logger import logger

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Safety check
if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("Missing BOT_TOKEN or CHAT_ID in .env file")

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def send_report(report_path):
    try:
        with open(report_path, "rb") as doc:
            bot.send_document(CHAT_ID, doc)

        logger.info("Report sent to Telegram successfully.")

    except Exception as e:
        logger.error(f"Failed to send report: {e}")