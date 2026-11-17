from delivery_strategy import DeliveryStrategy


class CourierDelivery(DeliveryStrategy):
    def get_cost(self, order): return 500.0
    def get_estimated_time(self, order=None): return "1-2 дня"
    def is_available(self, order): return order.total_weight <= 20.0
    def get_name(self): return "Курьер"
