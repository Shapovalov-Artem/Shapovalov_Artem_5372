from __future__ import annotations
import copy
from price import Price
from quantity import Quantity
from weight import Weight
from product_type import ProductType


class Product:
    _next_id = 1

    def __init__(self, id: int, name: str, category: str, price: int,
                 quantity: int, weight: float, type_: ProductType):
        if type_ is None:
            raise ValueError("У товара должен быть тип")
        self._id = id
        self._name = name
        self._category = category
        self._type = type_
        self._price = Price(int(price))
        self._current_price = Price(int(price))
        self._quantity = Quantity(quantity)
        self._weight = Weight(weight)

    @classmethod
    def generate_id(cls) -> int:
        value = Product._next_id
        Product._next_id += 1
        return value

    @classmethod
    def from_type(cls, id: int, quantity: int, type_: ProductType,
                  current_price=None) -> "Product":
        #Товар на основе общего типа из пула
        if type_ is None:
            raise ValueError("У товара должен быть тип")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        price = current_price if current_price is not None else type_.base_price
        return Product(id, type_.category, type_.category, int(price),
                       quantity, type_.base_weight * quantity, type_)

    def __copy__(self):
        new = type(self).__new__(type(self))
        new.__dict__.update(self.__dict__)
        new._price = Price(self._price.value)
        new._current_price = Price(self._current_price.value)
        new._quantity = Quantity(self._quantity.value)
        new._weight = Weight(self._weight.value)
        return new

    def clone(self) -> "Product":
        return copy.copy(self)

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def category(self): return self._category
    @property
    def type(self): return self._type
    @property
    def price_value(self): return self._price.value
    @property
    def quantity_value(self): return self._quantity.value
    @property
    def weight_value(self): return self._weight.value
    @property
    def quantity(self): return self._quantity.value
    @property
    def weight(self): return self._weight.value
    @property
    def current_price(self): return self._current_price.value
    @property
    def total_price(self): return self._current_price.value * self._quantity.value

    def get_weight(self) -> float: return self._weight.value
    def get_total_price(self) -> int: return self.total_price

    def change_quantity(self, delta: int):
        cur = self._quantity.value
        if cur + delta < 0:
            raise ValueError("Resulting quantity can't be negative")
        self._quantity.value = cur + delta

    def set_price(self, new_price: Price):
        self._price = new_price
        self._current_price = Price(new_price.value)
