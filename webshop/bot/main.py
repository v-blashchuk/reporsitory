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
from .models import Text, Products, Category, Cart, User
from .keyboards import START_KB, CATEGORIES_KB
from .lookups import category_lookup, separator, product_lookup, korzina_lookup, prod_discount_lookup, cart_lookup, order_lookup


bot = TeleBot("1155368557:AAFKQ1HoAJKffzFOyzD7IFUwIHpCQwT8v_k")


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['my_cart'])
def cart(message):
    chat_id = message.from_user.id
    try:
        current_cart = Cart.objects.get(chat_id=chat_id, finish=False)
        prods = current_cart.products
        quants = current_cart.quantity
        dict = {}
        for p in prods:
            print(p)
        for q in quants:
            print(q)
        for p, q in zip(prods, quants):
            product = Products.objects.get(id = p)
            name = product.title
            dict[name]=q
        print(dict)
        bot.send_message(message.chat.id, f"Товары в корзине:")
        bot.send_message(message.chat.id, f"----------------------")
        msg = [bot.send_message(message.chat.id, f"{name} - {quant} (шт/кг)\n ") for name, quant in dict.items()]
        bot.send_message(message.chat.id, f"----------------------")
        dict.clear()

    except Exception:
        bot.send_message(message.chat.id, f"Ваша корзина на данный момент пуста!")

    kb = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("Очистить Корзину", callback_data=f'{cart_lookup}{separator}{chat_id}')
    button_2 = InlineKeyboardButton("Отправить заказ!", callback_data=f'{order_lookup}{separator}{chat_id}')
    kb.add(button_1, button_2)
    bot.send_message(message.chat.id, text="Выберите действие с корзиной:", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] ==cart_lookup)
def cart_clear(call):
    chat_id=call.from_user.id
    current_cart = Cart.objects.get(chat_id=chat_id, finish=False)
    current_cart.update(set__products=[])
    current_cart.update(set__quantity=[])
    current_cart.save()
    bot.send_message(call.message.chat.id, f"Корзина очищена!")


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] ==order_lookup)
def cart_order(call):
    chat_id=call.from_user.id
    current_cart = Cart.objects.get(chat_id=chat_id, finish=False)
    current_cart.update(set__finish=True)
    current_cart.save()
    bot.send_message(call.message.chat.id, f"Заказ отправлен!\nС вами свяжется менеджер, спасибо.")


@bot.message_handler(content_types=['text'], func=lambda message: message.text == START_KB['discount_products'])
def discount_products(message):

    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(f'{prod.title} -{prod.discount}%', callback_data=f'{prod_discount_lookup}{separator}{prod.id}') for prod in Products.objects(discount__ne=0, in_stock=True)]
    kb.add(*buttons)
    bot.send_message(message.chat.id, text="Товары со скидкой:", reply_markup=kb)


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

    button = [InlineKeyboardButton(f'Заказать - {product.title}', callback_data=f'{korzina_lookup}{separator}{prod_id}{separator}{product.id}')]
    kb.add(*button)
    bot.send_message(call.message.chat.id, f"Описание товара:\n\nНазвание товара: {product.title}\nОписание товара: {product.description}\nЦена товара: {product.price}", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == korzina_lookup)
def zakaz_click(call):
    print(call)
    id_prod1= call.data.split(separator)[2]
    chat_id = call.from_user.id
    print(id_prod1)
    try:
        Cart.objects.get(chat_id=chat_id, finish=False) != 0
        active = Cart.objects.get(chat_id=chat_id, finish=False)
        active.products.append(id_prod1)
        active.save()
    except Exception:
        new_cart = Cart.objects.create(products=[id_prod1], chat_id=chat_id)

    msg = bot.send_message(call.message.chat.id, 'Введите количество или вес, сколько хотите заказать:')
    bot.register_next_step_handler(msg, get_quantity)


@bot.message_handler(content_types=['text'], func=lambda message: message.text != '/start')
def get_quantity(message):
    print(message)
    quantity = message.text
    chat_id = message.from_user.id
    cart = Cart.objects.get(chat_id=chat_id, finish=False)
    cart.quantity.append(quantity)
    cart.save()
    bot.reply_to(message, f"Спасибо, товар добавлен в корзину!" )



@bot.callback_query_handler(func=lambda call: call.data.split(separator)[0] == prod_discount_lookup)
def prod_discount__click(call):
    print(call.data)
    prod_id = call.data.split(separator)[1]
    print(prod_id)
    kb = InlineKeyboardMarkup()
    product = Products.objects.get(id=prod_id)
    button = [InlineKeyboardButton(f'Заказать - {product.title}', callback_data=f'{korzina_lookup}{separator}{product.id}')]
    kb.add(*button)
    bot.send_message(call.message.chat.id, f"Описание товара:\n\nНазвание товара: {product.title}\nОписание товара: {product.description}\nЦена товара: {product.price}\nСкидка на товар: {product.discount}", reply_markup=kb)


@bot.message_handler(commands=['start'])
def start(message):
    txt = Text.objects.get(title=Text.TITLES['greetings']).body
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(*[KeyboardButton(text=text) for text in START_KB.values()])
    bot.send_message(message.chat.id, txt, reply_markup=kb)
    user_id = message.from_user.id
    try:
        new_user = User.objects.get(user_id=user_id)
        name = new_user.name
        bot.send_message(message.chat.id, f"{name}, вы уже зарегистрированы в магазине, приступайте к заказу товара!", reply_markup=kb)
    except Exception:
        msg = bot.send_message(message.chat.id, 'Давайте пройдем быструю регистрацию, перед началом покупок.\nПожалуйста, введите свое имя:')
        bot.register_next_step_handler(msg, get_name_step)


@bot.message_handler(content_types=['text'])
def get_name_step(message):
    print(message)
    name = message.text
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = message.from_user.id
    new_user = User.objects.create(user_id=user_id, name=name, first_name=first_name, last_name=last_name)
    new_user.save()
    print(name, first_name, last_name, user_id)
    msg = bot.reply_to(message, f"Спасибо, {name}!\nВведите ваш контактный номер телефона:" )
    bot.register_next_step_handler(msg, get_telephone)


@bot.message_handler(content_types=['text'])
def get_telephone(message):
    print(message)
    telephone = str(message.text)
    user_id = message.from_user.id
    print(telephone)
    new_user = User.objects.get(user_id=user_id)
    new_user.update(telephone=telephone)
    new_user.save()
    msg = bot.reply_to(message, f"Спасибо!\nВведите компанию где работаете:" )
    bot.register_next_step_handler(msg, get_company_name)



@bot.message_handler(content_types=['text'])
def get_company_name(message):
    print(message)
    company_name = message.text
    user_id = message.from_user.id
    new_user = User.objects.get(user_id=user_id)
    new_user.update(company=company_name)
    new_user.save()
    msg = bot.reply_to(message, f"Отлично!\nТеперь введите адрес куда нужно будет доставлять заказы:")
    bot.register_next_step_handler(msg, get_address)


@bot.message_handler(content_types=['text'])
def get_address(message):
    print(message)
    address = message.text
    user_id = message.from_user.id
    new_user = User.objects.get(user_id=user_id)
    new_user.update(address_company=address)
    new_user.save()
    bot.send_message(message.chat.id, "Спасибо за регистрацию, теперь можно приступить к заказам!\nПерейдите в Категории для выбора продуктов.")



def start_bot():
    bot.polling()

if __name__=='__main__':
    start_bot()


