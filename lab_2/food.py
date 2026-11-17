import copy
from product import Product
from product_type import ProductType


class Food(Product):
    CATEGORY = "Food"

    def __init__(self, name, price, qty, weight):
        super().__init__(Product.generate_id(), name, self.CATEGORY, price, qty, weight,
                         ProductType.get_type(self.CATEGORY))


class Milk(Food):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "Milk":
        return copy.copy(self)


class Bread(Food):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "Bread":
        return copy.copy(self)
