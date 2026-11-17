from delivery_strategy import DeliveryStrategy


class PostDelivery(DeliveryStrategy):
    def get_cost(self, order): return 200.0
    def get_estimated_time(self, order=None): return "5-10 дней"
    def is_available(self, order): return order.total_weight <= 10.0
    def get_name(self): return "Почта"
