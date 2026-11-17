from discount_strategy import DiscountStrategy


class CashbackDiscount(DiscountStrategy):
    def apply(self, order):
        order.add_cashback((order.items_price - order.discount_amount) * 0.05)

    def get_name(self): return "Cashback 5%"
