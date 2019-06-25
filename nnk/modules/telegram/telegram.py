import telegram
bot = telegram.Bot(token='TOKEN')  # get the token
# TODO VERY IMPORTANT: DONT COMMIT THE TOKEN ITSELF!
# pull it from configurator or smth
print(bot.get_me())  # prints basic data about bots, used for testing

# most likely the telegram class will wrap around existing class providing:
#   blocking methods for getting messages, the telegramservice will thread them if needed
#   class will require the token to instantiate
#   perhaps some other methods as needed

# the wrapper will obtain the token, build the module and thread needed methods on start
from telegram.ext import Updater
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

