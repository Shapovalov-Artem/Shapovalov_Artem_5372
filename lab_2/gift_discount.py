from discount_strategy import DiscountStrategy
from product import Product
from product_type import ProductType


class GiftDiscount(DiscountStrategy):
    def apply(self, order):
        # подарок: кружка с нулевой ценой, id берём из общего генератора
        gift = Product.from_type(Product.generate_id(), 1, ProductType.get_type("mug"), 0)
        order.add_item(gift)

    def get_name(self): return "Подарок (кружка)"
