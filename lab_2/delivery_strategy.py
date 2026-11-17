from __future__ import annotations
from abc import ABC, abstractmethod


class DeliveryStrategy(ABC):
    @abstractmethod
    def get_cost(self, order): ...

    @abstractmethod
    def get_estimated_time(self, order=None): ...

    @abstractmethod
    def is_available(self, order): ...

    @abstractmethod
    def get_name(self): ...

    def __lshift__(self, order):
        from order import Order  # локальный импорт, чтобы не было цикла
        if not isinstance(order, Order):
            return NotImplemented
        order.set_delivery(self)
        return order