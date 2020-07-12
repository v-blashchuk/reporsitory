from models import Text


def init_text():
    Text.objects.create(
        title=Text.TITLES['greetings'],
        body='Рады приветствовать Вас в нашем магазине!'
    )

    Text.objects.create(
        title=Text.TITLES['cart'],
        body='Вы перешли в корзину:'
    )

if __name__ == '__main__':
    init_text()