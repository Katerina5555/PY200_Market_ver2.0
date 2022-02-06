import random
from typing import Union


class Category:
    list_of_categories = []

    def __init__(self, name=None):
        """
        Создание атрибутов класса Категория
        :param name: наименование категории
        :parameter self.product: для регистрации продуктов
        выбранной категории
        """
        self.name = name
        self.product = []
        self.list_of_categories.append(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def print_products_in_category(self):
        """
        :return: выводит информацию об имеющихся
        товарах выбранной категории
        """
        print(f'В магазине по категории {self.name} доступны следующие товары:')
        for number, category in enumerate(self.product, 1):
            print(number, "-", category)

    @classmethod
    def print_categories(cls):
        """
        выводит список доступных категорий
        :return: переходит на метод выбора конкретной категории
        """
        for number, category in enumerate(cls.list_of_categories, 1):
            print(number, "-", category)
        return Category.choose_category()

    @classmethod
    def choose_category(cls):
        """
        выводит запрос на выбор требуемой категории
        :return: переход на метод вспомогательного
        класса для заказа продукта и добавления в корзину
        """
        search_category = int(input("Введите номер категории")) - 1
        if search_category > len(cls.list_of_categories):
            raise ValueError("Указано значение за"
                             "пределами отраженного списка")
        else:
            category = Category.list_of_categories[search_category]
            return HelpToCategory.help_to_purchase(category)


class HelpToCategory(Category):
    cost = 0

    @classmethod
    def help_to_purchase(cls, category):
        """
        метод для оформления покупок
        :param category: выбранная категория товара
        :return: если приобретается один товар -
        завершает оформление покупки и отображает приобретенный
        товар и стоимость к оплате
        - если несколько: выводит список товаров в корзине и
        их стоимость, для продолжения покупок направляет
        в метод распечатки категорий
        """
        list_of_products = []
        # Category.print_products_in_category(category)
        list_of_products.append(Category.print_products_in_category(category))
        search_product = int(input("Введите номер продукта")) - 1

        if search_product > len(list_of_products):
            raise ValueError("Указано значение за"
                             "пределами отраженного списка")
        else:
            product = category.product[search_product]
            HelpToCategory.cost += product.price
            print(f'Вы заказали {product.name}')
        Basket.product_in_basket.append((product.name, product.price,
                                         "категория: " + product.category.name))
        print(Basket.product_in_basket)
        print(f"В корзине товаров на сумму {HelpToCategory.cost} рублей")
        answer = input("Закончить формирование покупок (да или нет)?")
        if answer == "да":
            print(Basket.product_in_basket)
            print(f"К оплате {HelpToCategory.cost} рублей")
        else:
            return f'{Category.print_categories()}'


class Product:
    list_of_products = []

    def __init__(self, name: str, price: int, rating: int, category: Category):
        """
        создание атрибутов класса Товар
        :param name: наименование товара
        :param price: цена товара
        :param rating: рейтинг
        :param category: категория к которой относится товар, для сортировки
        в классе Категория
        """
        self.name = name
        self.price = price
        self.rating = rating
        self.category = None
        self.no_category(category)
        self.list_of_products.append(self)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.price}, {self.rating}, ' \
               f'{self.category.name})'

    def __str__(self):
        return f'Товар: {self.name}, цена: {self.price}, ' \
                f'рейтинг {self.rating}, {self.category.name}'

    def no_category(self, category):
        if isinstance(category, Category):
            category.product.append(self)
            self.category = category
        else:
            raise ValueError("Указанная категория отсутсвует")

    @classmethod
    def print_products(cls):
        """отдельный метод - выводит все доступные товары,
        вне зависимости от категорий. С другими методами
        пока не взаимодействует"""
        for number, product in enumerate(cls.list_of_products, 1):
            print(number, "-", product)


class Basket:
    """
    Пустая корзина для начала покупок
    """
    product_in_basket = []


class User:
    list_of_users = {}

    def __init__(self, login: Union[int, str], password: Union[int, str]):
        """
        создание атрибутов Пользователя
        :param login:
        :param password:
        Хранение логина и пароля осуществляется в словаре
        """
        self.login = login
        self.password = password
        self.basket = Basket()
        self.list_of_users[self.login] = self.password

    @classmethod
    def enter_in_market(cls, login, password):
        """
        метод начала покупки
        :param login: вводится через инпут
        :param password: вводится через инпут
        :return: если пользователь отсутствует - ошибка;
        если пользователь зарегистрирован и пара
        (логин-пароль) верные - начинается процесс покупки.
        Выводится список возможных категорий из класса
        Категории
        """
        if not (login in User.list_of_users):
            raise ValueError('Такой пользователь не зарегистрирован')
        else:
            if password == User.list_of_users[login]:
                print("Можно начинать покупки")
                print("Пользователь " + login + " авторизирован")
                return f'{Category.print_categories()}'
            else:
                raise ValueError("Пароль не соответствует")

    def __repr__(self):
        return f'{self.__class__.__name__}({self.login}, {self.password}, {self.basket})'

    def __str__(self):
        return f'Логин пользователя: {self.login}, Пароль: {self.password}, ' \
               f'в корзине: {self.basket}'


if __name__ == '__main__':
    user1 = User("IVAN", "12345")
    user2 = User("MARTA", "qwerty")
    category1 = Category("Мебель")
    category2 = Category("Овощи")
    category3 = Category("Фрукты")
    product1 = Product("Стол", 2804, random.randint(0, 10), category1)
    product2 = Product("Стул", 1500, random.randint(0, 10), category1)
    product3 = Product("Морковь", 150, random.randint(0, 10), category2)
    product4 = Product("Капуста", 90, random.randint(0, 10), category2)
    product5 = Product("Яблоко", 104, random.randint(0, 10), category3)
    product6 = Product("Апельсин", 110, random.randint(0, 10), category3)
    # Product.print_products()
    # Category.print_categories()
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    User.enter_in_market(login, password)





