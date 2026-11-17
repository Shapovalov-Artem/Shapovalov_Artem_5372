from discount_strategy import DiscountStrategy


class FreeDeliveryDiscount(DiscountStrategy):
    def apply(self, order):
        order.set_free_delivery(True)

    def get_name(self): return "Бесплатная доставка"
