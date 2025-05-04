import logging
from dotenv import load_dotenv
import os
import json

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from llm import myClient
from db import create_connection

load_dotenv()

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


client = myClient()
db_conn = create_connection("sm_app.sqlite")

tools = [json.load()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I am an expense tracker bot. Just text me your expenses and I will take care of storing, sorting and analysing your regular expenses"
    )

async def recurring_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    command to add a regular expense to the current account. The message should contain:
    - amount
    - period/interval
    - description

    If something is missing the bot should ask clarifying questions.
    """
    pass

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    handles all other text messages by forwarding to model
    """

    message = update.message.text
    sender = update.message.chat.first_name

    logging.info(f"receiving message {message} from {sender}")

    reply = await client.answer(message)

    logging.info(f"this is the reply {reply}")

    await update.message.reply_text(reply)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)

    application.add_handler(start_handler)
    application.add_handler(text_handler)

    application.run_polling()
