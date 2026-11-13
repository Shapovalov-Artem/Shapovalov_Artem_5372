from product import Product


class Clothing(Product): pass


class TShirt(Clothing):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Clothing")
        self.__dict__.update(p.__dict__)
    def clone(self): return self.__copy__()


class Jacket(Clothing):
    def __init__(self, name, price, qty, weight):
        p = Product.from_factory(name, price, qty, weight, "Clothing")
        self.__dict__.update(p.__dict__)
    def clone(self): return self.__copy__()