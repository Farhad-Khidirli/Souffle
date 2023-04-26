from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from key import tg_token


# Define the command handler for the /start command
def start(update, context):
    """Handler for the /start command"""
    first_name = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Hello {first_name}!")


# Define the message handler for all other messages
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def start_telegram_bot():
    # Create the updater and dispatcher objects
    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    # Add the handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    # Start the bot
    updater.start_polling()


# Call the start_telegram_bot() method to start the bot
start_telegram_bot()
