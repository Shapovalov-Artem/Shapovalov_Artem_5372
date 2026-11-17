import copy
from product import Product
from product_type import ProductType


class Electronics(Product):
    CATEGORY = "Electronics"

    def __init__(self, name, price, qty, weight):
        super().__init__(Product.generate_id(), name, self.CATEGORY, price, qty, weight,
                         ProductType.get_type(self.CATEGORY))


class Smartphone(Electronics):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "Smartphone":
        return copy.copy(self)


class Laptop(Electronics):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "Laptop":
        return copy.copy(self)
