import os
import random

from telegram import Bot, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Dispatcher, Updater, MessageHandler, Filters, CommandHandler
from telegram.update import Update

from words import words


PASSWORDS_COUNT = 5
BOT_TOKEN = os.environ['BOT_TOKEN']


HELP_MESSAGE = '''
Generates XKCD passwords. See https://xkcd.com/936/

No logs.

Custom password masks available.
· %d for digit
· %w for lowercased word
· %W for Capitalized word
· %C for UPPERCASED word

Example:
`%w-%w-%w-%w` outputs `escalators-better-vaccinate-nonabsorbent`
`%w-%W-%C-%d%d%d` outputs `carousels-Foreshadowing-DISHWATER-934`
'''


def generate_passwords(mask):
    passwords = []
    for i in range(PASSWORDS_COUNT):
        password = mask
        while '%w' in password:
            password = password.replace('%w', random.choice(words), 1)
        while '%W' in password:
            password = password.replace('%W', random.choice(words).capitalize(), 1)
        while '%C' in password:
            password = password.replace('%C', random.choice(words).upper(), 1)
        while '%d' in password:
            password = password.replace('%d', str(random.randint(0, 9)), 1)
        passwords.append('`{0}`'.format(password))
    return '\n\n'.join(passwords)


def message_handler(update, context):
    message = update.message
    message_text = message.text
    reply_markup = ReplyKeyboardMarkup([[message_text]], resize_keyboard=True)
    message.reply_text(
        text=generate_passwords(mask=message_text),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )


def start_command_handler(update, context):
    message = update.message
    message.reply_text(
        text=HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
    )
    default_mask = '%w-%w-%w-%w'
    reply_markup = ReplyKeyboardMarkup([[default_mask]], resize_keyboard=True)
    message.reply_text(
        text=generate_passwords(mask=default_mask),
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )


def help_command_handler(update, context):
    message = update.message
    message.reply_text(
        text=HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
    )


def set_handlers(dispatcher):
    any_message_handler = MessageHandler(Filters.text, message_handler)
    dispatcher.add_handler(any_message_handler)
    command_handler = CommandHandler('start', start_command_handler)
    dispatcher.add_handler(command_handler)
    help_handler = CommandHandler('help', help_command_handler)
    dispatcher.add_handler(help_handler)


def setup_dispatcher(token):
    bot = Bot(token)
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    set_handlers(dispatcher)
    return dispatcher


def main(request):
    if request.method == "POST":
        dispatcher = setup_dispatcher(token=BOT_TOKEN)
        update = Update.de_json(request.get_json(force=True), dispatcher.bot)
        dispatcher.process_update(update)
    return "ok"


if __name__ == '__main__':
    # DEBUG ONLY
    webhook_url = os.environ['WEBHOOK_URL']
    updater = Updater(token=BOT_TOKEN, use_context=True)
    set_handlers(updater.dispatcher)
    # updater.bot.set_webhook(os.environ.get('WEBHOOK_URL_PROD'))
    updater.bot.set_webhook(webhook_url)
    updater.start_webhook(listen='0.0.0.0',
                          port=4000,
                          url_path='/',
                          webhook_url=webhook_url)
