import decimal

import telegram
from telegram import *
from telegram.ext import *
from app import is_found_chat_id, register_for_telegram, get_user_by_id, get_balance, validate_pair, validate_address, \
    transfer as transfer_ethers
from key import tg_token
from twilio_verify import verify_number, send_verification
from email_verify import verify_email, send_email_otp

# define the start function and set a custom keyboard
# create a bot instance and initialize the token
bot = telegram.Bot(token=tg_token)

CANCEL, REGISTER, PRIVATE_KEY, SEND_PHONE_OTP, PHONE_NUMBER, EMAIL_ADDRESS, FINISH_REGISTRATION, VERIFY_NUMBER_OTP, VERIFY_EMAIL_OTP, TRANSFER, AMOUNT, RECIPIENT = range(
    12)


# define the start function and set a custom keyboard
def start(update, context):
    user_id = update.message.chat_id
    if is_found_chat_id(user_id):
        username = update.message.from_user.first_name
        update.message.reply_text(f'Welcome back, {username}! Call /transfer for Transfer💸')

    else:
        return REGISTER


def register(update, context):
    user_id = update.message.chat_id
    update.message.reply_text('Please, complete the registration to start using this bot.')
    public_address = update.message.reply_text('Enter your public address: ')
    return PRIVATE_KEY


def get_private_key(update, context):
    if validate_address(update.message.text):
        context.user_data['public_address'] = update.message.text
        private_key = update.message.reply_text('Enter your private key: ')
        return PHONE_NUMBER
    else:
        update.message.reply_text('Invalid public address, please enter correct one : ')
        return PRIVATE_KEY


def get_phone_number(update, context):
    if validate_pair(context.user_data['public_address'], update.message.text):
        context.user_data['private_key'] = update.message.text
        phone_number = update.message.reply_text('Enter your phone number: ')
        return SEND_PHONE_OTP
    else:
        update.message.reply_text('Provided address and/or key is incorrect, start again')
        return ConversationHandler.END


# TESTED, WORKING (TWILIO)
def send_phone_otp(update, context):
    context.user_data['phone_number'] = update.message.text
    # send_verification(context.user_data['phone_number'])
    update.message.reply_text('OTP successfully sent. Please enter the OTP: ')
    context.user_data['attempts'] = 3
    update.message.reply_text('Enter your email address: ')
    return EMAIL_ADDRESS
    # return VERIFY_NUMBER_OTP


def verify_number_otp(update, context):
    user_data = context.user_data
    status = verify_number(user_data['phone_number'], update.message.text)
    if status == 'approved':
        update.message.reply_text('OTP verification successful!')
        update.message.reply_text('Enter your email address: ')
        return EMAIL_ADDRESS
    else:
        user_data['attempts'] -= 1
        if user_data['attempts'] > 0:
            update.message.reply_text(
                f'Incorrect OTP. Please try again. You have {user_data["attempts"]} attempts left.')
            update.message.reply_text('Please enter the OTP: ')
            return VERIFY_NUMBER_OTP
        else:
            update.message.reply_text('Maximum number of attempts exceeded. Registration failed.')
            return ConversationHandler.END


# TEMPORARY UNAVAILABLE (SENDGRID)
def get_email_address(update, context):
    context.user_data['email_address'] = update.message.text
    send_email_otp(context.user_data['email_address'])

    update.message.reply_text('OTP successfully sent. Please enter the OTP: ')
    context.user_data['attempts'] = 3
    # return VERIFY_EMAIL_OTP
    return FINISH_REGISTRATION


def verify_email_otp(update, context):
    user_data = context.user_data
    if verify_email(update.message.text) == 'approved':
        update.message.reply_text('OTP verification successful!')
        return FINISH_REGISTRATION
    else:
        user_data['attempts'] -= 1
        if user_data['attempts'] > 0:
            update.message.reply_text(
                f'Incorrect OTP. Please try again. You have {user_data["attempts"]} attempts left.')
            update.message.reply_text('Please enter the OTP: ')
            return VERIFY_EMAIL_OTP
        else:
            update.message.reply_text('Maximum number of attempts exceeded. Registration failed.')
            return ConversationHandler.END


def end_registration(update, context):
    user_data = context.user_data
    update.message.reply_text('Thank you for completing the registration!')
    register_for_telegram(update.message.chat_id,
                          user_data['public_address'],
                          user_data['private_key'],
                          user_data['phone_number'],
                          user_data['email_address'])
    print(user_data)
    return ConversationHandler.END


def transfer(update, context):
    user_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("Yes", callback_data='yes'),
                 InlineKeyboardButton("No", callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('I heard that you would like to transfer money?', reply_markup=reply_markup)
    return TRANSFER


def transfer_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "yes":
        query.edit_message_text("Please enter the recipient's address or ID: ")
        return RECIPIENT
    else:
        query.edit_message_text("Cancelled.")
        return ConversationHandler.END


def recipient(update: Update, context: CallbackContext):
    _recipient = update.message.text
    if validate_address(_recipient):
        context.user_data['recipient'] = _recipient
        update.message.reply_text("Please enter the amount of money in ethers to send: ")
        return AMOUNT
    else:
        if _recipient.isdigit() and is_found_chat_id(int(_recipient)):
            context.user_data['recipient'] = get_user_by_id(int(_recipient))['public_address']
            update.message.reply_text("Please enter the amount of money in ethers to send: ")
            return AMOUNT
        else:
            return ConversationHandler.END


def amount(update: Update, context: CallbackContext):
    _amount = update.message.text
    user_id = update.message.chat_id
    _recipient = context.user_data['recipient']
    _balance = get_balance(user_id)
    if _balance > decimal.Decimal(_amount):
        # SEND OTP to NUMBER or EMAIL
        transfer_ethers(user_id, _recipient, _amount)
        update.message.reply_text(
            f"The amount of ethers to send is: {_amount}\nRecipient's address or ID: {_recipient}")
        return ConversationHandler.END
    else:
        update.message.reply_text(f"Insufficient funds. Your balance is: {_balance}\nPlease enter different amount: ")
        return AMOUNT


def info(update, context):
    user_id = update.message.chat_id
    username = update.message.from_user.first_name
    update.message.reply_text(f'Dear {username}, here is your information 📂')
    user_info = get_user_by_id(user_id)
    public_address = user_info['public_address']
    phone_number = user_info['phone_number']
    email = user_info['email_address']
    masked_number = phone_number[:6] + '*' * 5 + phone_number[-2:]

    if '@' in email:
        masked_email = email[0] + ''.join(['*' for _ in range(email.index('@') - 1)]) + email[email.index('@') - 1:]
    else:
        masked_email = email

    update.message.reply_text(f'Your user id is: {user_id}\n\n'
                              f'Your public address is: {public_address}\n\n'
                              f'Your phone number is: {masked_number}\n\n'
                              f'Your email is: {masked_email}')


def balance(update, context):
    user_id = update.message.chat_id
    _balance = get_balance(user_id)
    update.message.reply_text(f'Your balance is:\t💲{_balance} ethers')


def cancel(update, context):
    update.message.reply_text('Process cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def start_bot():
    updater = Updater(token=tg_token, use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('info', info),
                      CommandHandler('transfer', transfer), CommandHandler('balance', balance)],
        states={
            REGISTER: [MessageHandler(Filters.text, register)],
            PRIVATE_KEY: [MessageHandler(Filters.text, get_private_key)],
            PHONE_NUMBER: [MessageHandler(Filters.text, get_phone_number)],
            SEND_PHONE_OTP: [MessageHandler(Filters.text, send_phone_otp)],
            VERIFY_NUMBER_OTP: [MessageHandler(Filters.text, verify_number_otp)],
            EMAIL_ADDRESS: [MessageHandler(Filters.text, get_email_address)],
            VERIFY_EMAIL_OTP: [MessageHandler(Filters.text, verify_email_otp)],
            FINISH_REGISTRATION: [MessageHandler(Filters.text, end_registration)],
            TRANSFER: [CallbackQueryHandler(transfer_callback)],
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, recipient)],
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, amount)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        # per_message=True
    )

    updater.dispatcher.add_handler(conv_handler)
    # start the bot
    updater.start_polling()
    updater.idle()


start_bot()
