from telegram.ext import Updater
# $ pip install python-telegram-bot --upgrade # there is another package with similar name, do not mistake for this one

# most likely the telegram class will wrap around existing class providing:
#   blocking methods for getting messages, the telegramservice will thread them if needed
#   class will require the token to instantiate
#   perhaps some other methods as needed

# the wrapper will obtain the token, build the module and thread needed methods on start
def demo():
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher


    def start(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


    from telegram.ext import CommandHandler
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


    def echo(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


    from telegram.ext import MessageHandler, Filters
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)


class TelegramModule:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start_telegram(self):
        self.updater.start_polling()

    def add_handler(self, handler):
        self.dispatcher.add_handler(handler)
