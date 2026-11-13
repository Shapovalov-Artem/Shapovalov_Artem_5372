from __future__ import annotations
from attributes import Price, Quantity, Weight
from product_type import ProductType

class Product:
    _next_id = 1

    def __init__(self, id: int, quantity: int, type_: ProductType,
                 current_price=None):
        if type_ is None:
            raise ValueError("У товара должен быть тип")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self._id = id
        self._quantity = Quantity(quantity)
        self._weight = Weight(type_.base_weight * quantity)
        self._current_price = Price(int(current_price if current_price is not None
                                        else type_.base_price))
        self._type = type_
        self._name = type_.category
        self._category = type_.category
        self._price = self._current_price

    @classmethod
    def from_factory(cls, name: str, price: int, qty: int, weight: float,
                     category: str) -> "Product":
        obj = cls.__new__(cls)
        obj._id = Product._next_id
        Product._next_id += 1
        obj._name = name
        obj._price = Price(price)
        obj._quantity = Quantity(qty)
        obj._weight = Weight(weight)
        obj._category = category
        obj._current_price = Price(price)
        obj._type = None
        return obj

    def __copy__(self):
        new = Product.__new__(Product)
        new._id = self._id
        new._name = self._name
        new._category = self._category
        new._type = self._type
        new._price = Price(self._price.value)
        new._quantity = Quantity(self._quantity.value)
        new._weight = Weight(self._weight.value)
        new._current_price = Price(self._current_price.value)
        return new

    def clone(self): return self.__copy__()

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

    def change_quantity(self, delta: int):
        cur = self._quantity.value
        if cur + delta < 0:
            raise ValueError("Resulting quantity can't be negative")
        self._quantity.value = cur + delta

    def set_price(self, new_price: Price):
        self._price = new_price
        self._current_price = new_price