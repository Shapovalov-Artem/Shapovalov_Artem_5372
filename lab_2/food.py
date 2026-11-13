from product import Product


class Food(Product): pass


class Milk(Food):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Food")
        self.__dict__.update(p.__dict__)
    def clone(self): return self.__copy__()


class Bread(Food):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Food")
        self.__dict__.update(p.__dict__)
    def clone(self): return self.__copy__()