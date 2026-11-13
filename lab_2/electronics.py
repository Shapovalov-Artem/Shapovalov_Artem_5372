from product import Product

class Electronics(Product): pass

class Smartphone(Electronics):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Electronics")
        self.__dict__.update(p.__dict__)

    def clone(self):
        return self.__copy__()


class Laptop(Electronics):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Electronics")
        self.__dict__.update(p.__dict__)

    def clone(self):
        return self.__copy__()