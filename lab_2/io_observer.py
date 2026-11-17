from abc import ABC, abstractmethod


class IObserver(ABC):
    @abstractmethod
    def on_order_event(self, event): ...
