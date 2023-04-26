import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from key import tg_token

# Replace YOUR_TOKEN with your own Telegram bot token
bot = telegram.Bot(token=tg_token)


def start(update, context):
    """Handler for the /start command"""
    # Get the user's first name from the update object
    first_name = update.message.from_user.first_name
    # Send a greeting message to the user
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Hello {first_name}!")


def info(update, context):
    """Handler for the /info command"""
    # Get the user's chat ID
    chat_id = update.message.chat_id
    # Send a message with the user's chat ID
    context.bot.send_message(chat_id=chat_id, text=f"Your chat ID is {chat_id}")


def menu(update, context):
    """Handler for the /menu command"""
    # Create a list of menu options
    menu_options = [
        InlineKeyboardButton("Start", callback_data='start'),
        InlineKeyboardButton("Info", callback_data='info')
    ]
    # Create a keyboard with the menu options
    reply_markup = InlineKeyboardMarkup([menu_options])
    # Send a message with the menu options
    context.bot.send_message(chat_id=update.message.chat_id, text='Please select an option:', reply_markup=reply_markup)


def menu_button_callback(update, context):
    """Handler for the menu button"""
    query = update.callback_query
    # Check which button was clicked
    if query.data == 'start':
        # Send a greeting message
        first_name = query.message.chat.first_name
        context.bot.send_message(chat_id=query.message.chat_id, text=f"Hello {first_name}!")
    elif query.data == 'info':
        # Send the user's chat ID
        chat_id = query.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=f"Your chat ID is {chat_id}")


def main():
    """Main function to start the bot"""
    # Replace YOUR_TOKEN with your own Telegram bot token
    updater = Updater(token=tg_token, use_context=True)

    # Add a CommandHandler to handle the /start command
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Add a CommandHandler to handle the /info command
    updater.dispatcher.add_handler(CommandHandler('info', info))

    # Add a CommandHandler to handle the /menu command
    updater.dispatcher.add_handler(CommandHandler('menu', menu))

    # Add a CallbackQueryHandler to handle the menu button
    updater.dispatcher.add_handler(CallbackQueryHandler(menu_button_callback))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
