from webshop.bot import main
from webshop.bot.main import start_bot, bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update

from telebot import TeleBot

app = Flask(__name__)

start_bot()

if __name__ == '__main__':
    start_bot()
