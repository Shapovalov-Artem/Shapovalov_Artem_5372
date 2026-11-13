from abc import ABC, abstractmethod
class Delivery(ABC):
    @abstractmethod
    def get_cost(self, order): ...
    @abstractmethod
    def get_estimated_time(self): ...
    @abstractmethod
    def is_available(self, order): ...
    @abstractmethod
    def get_name(self): ...

from delivery import Delivery
class CourierDelivery(Delivery):
    def get_cost(self, order): return 500.0
    def get_estimated_time(self): return "1-2 дня"
    def is_available(self, order): return order.total_weight <= 20.0
    def get_name(self): return "Курьер"

from delivery import Delivery
class PickupDelivery(Delivery):
    def get_cost(self, order): return 0.0
    def get_estimated_time(self): return "1-3 дня"
    def is_available(self, order): return True
    def get_name(self): return "Самовывоз"

from delivery import Delivery
class PostDelivery(Delivery):
    def get_cost(self, order): return 200.0
    def get_estimated_time(self): return "5-10 дней"
    def is_available(self, order): return order.total_weight <= 10.0
    def get_name(self): return "Почта"