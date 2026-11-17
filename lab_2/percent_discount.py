from discount_strategy import DiscountStrategy


class PercentDiscount(DiscountStrategy):
    def apply(self, order):
        order.add_discount_amount((order.items_price - order.discount_amount) * 0.10)

    def get_name(self): return "Скидка 10%"
