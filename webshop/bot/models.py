import mongoengine as me
import datetime

me.connect('webshop_bot_new')


class User(me.Document):
    user_id = me.IntField(me_field='id')
    name = me.StringField(min_length=1, max_length=50)
    first_name = me.StringField(min_length=1, max_length=50)
    last_name = me.StringField(min_length=1, max_length=50)
    company = me.StringField(min_length=1, max_length=50)
    address_company = me.StringField(min_length=1, max_length=100)
    telephone = me.StringField(min_length=1, max_length=100)



class Category(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2, max_length=4096)
    subcategories = me.ListField(me.ReferenceField('self'))
    parent = me.ReferenceField('self', default=None)

    @classmethod
    def get_root_category(cls):
        cls.objects()

    @property
    def is_parent(self):
        return bool(self.subcategories)

    def get_products(self):
        Products.objects(category=self)


class Cart(me.Document):
    chat_id = me.IntField(me_field='id')
    products = me.ListField(min_length=2 ,max_length=4096)
    quantity = me.ListField(min_length=2 ,max_length=4096)   
    price = me.FloatField(default=0) 
    date = me.DateTimeField(default=datetime.datetime.now())
    finish = me.BooleanField(default=False)
    


    def active_cart(self, chat_id):
        Cart.objects.get(chat_id=chat_id, finish=False)

    def add_product(self, cart, product_id):
        pass




class Products(me.Document):
    title = me.StringField(min_length=1, max_length=512)
    description = me.StringField(min_length=2 ,max_length=4096)
    created = me.DateField(default=datetime.datetime.now())
    price = me.DecimalField(required=True)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    image = me.FileField(required=False, default=None)
    category = me.ReferenceField(Category)

    @property
    def extended_price(self):
        return self.price * (100 - self.discount) / 100

    @classmethod
    def get_discount_products(cls):
        return cls.objects(discount__ne=0, in_stock=True)

    @classmethod
    def get_category_products(cls, category):
        return cls.objects(category=category)



class Text(me.Document):

    TITLES = {
        'greetings': 'Текст приветствия',
        'cart': 'Текст корзины'
    }
    title = me.StringField(min_length=1, max_length=256, choices=TITLES.values(), unique=True)
    body = me.StringField(min_length=1, max_length=4096)


def fill_db():
    Products.objects.create(title='Помидор', description='Помидор крассный', price=100 , category='Овощи')
    Products.objects.create(title='Огурец', description='Огурцец стандартный', price=190 , category='Овощи')
    Products.objects.create(title='Баклажан', description='Баклажан стандартный', price=10 , category='Овощи')
    Products.objects.create(title='Морковь', description='Морковь стандартная', price=11 , category='Овощи')
    Products.objects.create(title='Капуста', description='Капуста стандартная', price=16 , category='Овощи')
    Products.objects.create(title='Яблоко', description='Яблоко РедГолд', price=100 , category='Фрукты')
    Products.objects.create(title='Груша', description='Груша украинская', price=200 , category='Фрукты')
    Products.objects.create(title='Виноград', description='Виноград КишьМышь', price=250 , category='Фрукты')
    Products.objects.create(title='Слива', description='Слива большая', price=345 , category='Фрукты')
    Products.objects.create(title='Укроп', description='Укроп', price=20 , category='Зелень')
    Products.objects.create(title='Петрушка', description='Петрушка', price=100 , category='Зелень')
    Products.objects.create(title='Руккола', description='Руккола', price=100 , category='Зелень')
    Products.objects.create(title='Базилик', description='Базилик', price=100 , category='Зелень')
    Products.objects.create(title='Тимьян', description='Тимьян', price=100 , category='Зелень')
    Products.objects.create(title='Розмарин', description='Розмарин', price=100 , category='Зелень')
    Products.objects.create(title='Апельсин', description='Апельсин', price=100 , category='Цитрусы')
    Products.objects.create(title='Лимон', description='Лимон', price=100 , category='Цитрусы')
    Products.objects.create(title='Манго', description='Манго', price=100 , category='Цитрусы')
    Products.objects.create(title='Авокадо', description='Авокадо', price=100 , category='Цитрусы')
    Products.objects.create(title='Ананас', description='Ананас', price=100 , category='Цитрусы')
    Products.objects.create(title='Лайм', description='Лайм', price=100 , category='Цитрусы')
    Products.objects.create(title='Томат в соб. соку', description='Томат в собственном соку', price=100 , category='Консервация')
    Products.objects.create(title='Огурец сол.', description='Огурец соленый', price=100 , category='Консервация')
    Products.objects.create(title='Ананас консерв.', description='Ананас консервированный', price=100 , category='Консервация')
    Products.objects.create(title='Томат', description='Томат', price=100 , category='Консервация')
    Products.objects.create(title='Кетчуп', description='Кетчуп', price=100 , category='Консервация')
    Products.objects.create(title='Топинг малин.', description='Топинг малиновый', price=100 , category='Консервация')
    Products.objects.create(title='Соль', description='Соль 1кг', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Сахар', description='Сахар 1кг', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Мука', description='Мука 5кг', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Рис басм.', description='Рис басмати', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Крохмал кукур.', description='Крохмал кукурузный', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Яйцо кур.', description='Яйцо куриное', price=100 , category='Бакалея, крупы, яйцо')
    Products.objects.create(title='Масло подс.', description='Масло подсолнечное', price=100 , category='Бакалея, крупы, яйцо')


if __name__ == '__main__':
    fill_db()
    # Text(title='Текст приветствия', body='Приветствую Вас в магазине!')
    # Text(title='Текст приветствия', body='Рады Вас видеть в нашем магазине!')