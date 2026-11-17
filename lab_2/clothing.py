import copy
from product import Product
from product_type import ProductType


class Clothing(Product):
    CATEGORY = "Clothing"

    def __init__(self, name, price, qty, weight):
        super().__init__(Product.generate_id(), name, self.CATEGORY, price, qty, weight,
                         ProductType.get_type(self.CATEGORY))


class TShirt(Clothing):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "TShirt":
        return copy.copy(self)


class Jacket(Clothing):
    def __init__(self, name, price, qty, weight):
        super().__init__(name, price, qty, weight)

    def clone(self) -> "Jacket":
        return copy.copy(self)
