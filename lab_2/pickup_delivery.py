from delivery_strategy import DeliveryStrategy


class PickupDelivery(DeliveryStrategy):
    def get_cost(self, order): return 0.0
    def get_estimated_time(self, order=None): return "1-3 дня"
    def is_available(self, order): return True
    def get_name(self): return "Самовывоз"
