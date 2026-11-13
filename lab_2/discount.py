from abc import ABC, abstractmethod
from product import Product
from product_type import ProductType

class Discount(ABC):
    @abstractmethod
    def apply(self, order): ...
    @abstractmethod
    def get_name(self): ...

class PercentDiscount(Discount):
    def apply(self, order): order.add_discount_amount((order.items_price - order.discount_amount) * 0.10)
    def get_name(self): return "Скидка 10%"

class CashbackDiscount(Discount):
    def apply(self, order): order.add_cashback((order.items_price - order.discount_amount) * 0.05)
    def get_name(self): return "Cashback 5%"

class FreeDeliveryDiscount(Discount):
    def apply(self, order): order.set_free_delivery(True)
    def get_name(self): return "Бесплатная доставка"

class GiftDiscount(Discount):
    def apply(self, order):
        order.add_item(Product(9000, 1, ProductType.get_type("mug"), 0.0))
    def get_name(self): return "Подарок (кружка)"