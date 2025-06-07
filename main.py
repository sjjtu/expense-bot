import logging
from dotenv import load_dotenv
import os
import json

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, DictPersistence

from llm import myClient
from db import create_connection, add_record

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


#client = myClient(api_key=os.getenv("OPENAI_API_KEY"), model="google/gemma-2-27b", base_url="http://127.0.0.1:1234/v1")
client = myClient(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4.1")
db_conn = create_connection("sm_app.sqlite")

tools = []

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

def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    handles all other text messages by forwarding to model
    """

    message = update.message.text
    sender = update.message.chat.first_name
    history = context.chat_data.get("history", [])


    logging.info(f"receiving message {message} from {sender}")
    logging.info(f"this the {context.chat_data=}")
    reply = client.answer(message, history)
    answer = reply.content # get actual answer content

    if not answer: # if answer is empty we are having a tool call
        answer = "record is added"

    logging.info(f"this is the reply {reply}")

    if reply.tool_calls[0]:
        tool_call = reply.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        logger.debug(f"tool call is: {tool_call}")
        if tool_call.function.name == "add_record":
            try:
                add_record(conn=db_conn, chat_id=update.effective_chat.id, amount=args["amount"], date=args["date"],
                       description=args["description"], category=args["category"])
            except Exception as e:
                logger.debug(e)
                answer = "something went wrong"


    # Get the current history or create a new list if it doesn't exist


    # Append the new message to the history
    history.extend(
        [{
            "role": "user",
            "content": update.message.text,
        },
        {
            "role": "system",
            "content": answer
        }]
    )

    # Save the updated history back to chat_data
    context.chat_data["history"] = history

    return update.message.reply_text(answer)


if __name__ == '__main__':
    persistence = DictPersistence()
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).persistence(persistence).build()

    start_handler = CommandHandler('start', start)
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)

    application.add_handler(start_handler)
    application.add_handler(text_handler)

    application.run_polling()
