import webshop.bot.main
from webshop.bot import config
# from .webshop.bot import main, config
# from reporsitory.webshop.bot.main import start_bot, bot
from flask import Flask, request, abort
from telebot.types import Update
# from reporsitory.webshop.bot.main import start_bot
# import webshop.bot.main
from telebot import TeleBot

app = Flask(__name__)

webshop.bot.main.start_bot()


if __name__ == '__main__':
    app.run(debug=True)