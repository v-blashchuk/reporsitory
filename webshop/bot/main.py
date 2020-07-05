# from telebot import TeleBot
# from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# # import config
# import models, keyboards
# from models import Text, Products, Category
# from keyboards import START_KB, CATEGORIES_KB
# from lookups import category_lookup, separator

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# import config
from . import models, keyboards
from .models import Text, Products, Category
from .keyboards import START_KB, CATEGORIES_KB
from .lookups import category_lookup, separator, product_lookup, korzina_lookup


bot = TeleBot("1155368557:AAFKQ1HoAJKffzFOyzD7IFUwIHpCQwT8v_k")


@bot.message_handler(commands=['start'])
def start(message):
    txt = Text.objects.get(title=Text.TITLES['greetings']).body
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(message.chat.id, txt, reply_markup=kb)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['category'])
def categories(message):
    kb = InlineKeyboardMarkup(row_width=2)
    roots = Category.objects()
    buttons = [InlineKeyboardButton(text=category.title, 
                                    callback_data=f'{category_lookup}{separator}{category.id}') 
                                    for category in roots]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text='Выберите категорию:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] ==category_lookup)
def category_click(call):
    category_id = call.data.split(separator)[1]
    cat = Category.objects.get(id=category_id).title
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(prod.title, callback_data=f'{product_lookup}{separator}{prod.id}') for prod in Products.objects(category=category_id)]
    kb.add(*buttons)
    bot.send_message(call.message.chat.id, f"Выберите продукты из категории {cat}:", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == product_lookup)
def prod_click(call):
    print(call.data)
    prod_id = call.data.split(separator)[1]
    print(prod_id)
    kb = InlineKeyboardMarkup()
    product = Products.objects.get(id=prod_id)

    button = [InlineKeyboardButton(f'Заказать - {product.title}', callback_data=f'{korzina_lookup}{separator}{product.id}')]
    kb.add(*button)
    bot.send_message(call.message.chat.id, f"Описание товара:\n\nНазвание товара: {product.title}\nОписание товара: {product.description}\nЦена товара: {product.price}", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == korzina_lookup)
def zakaz_click(call):
    print(call.data)


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['my_cart'])
def cart(message):
    bot.send_message(message.chat.id, "Вы перейшли в корзину!")


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['discount_products'])
def discount_products(message):
    bot.send_message(message.chat.id, "Товары со скидкой:")



def start_bot():
    bot.polling()

if __name__=='__main__':
    start_bot()


