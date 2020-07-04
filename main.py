from reporsitory.webshop.bot import main, config
from reporsitory.webshop.bot.main import start_bot, bot
from flask import Flask, request, abort
from telebot.types import Update


app = Flask(__name__)




if __name__ == '__main__':
    app.run(debug=True)