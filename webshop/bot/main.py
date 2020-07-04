from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from reporsitory.webshop.bot import config

from ..db import models
from ..db.models import Text, Products
from .keyboards import START_KB


bot = TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    txt = Text.objects.get(title=Text.TITLES['greetings']).body

    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])

    bot.send_message(message.chat.id, txt, reply_markup=kb)



def start_bot():
    bot.polling()

if __name__=='__main__':
    start_bot()


