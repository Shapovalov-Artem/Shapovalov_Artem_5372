from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, order): ...

    @abstractmethod
    def get_name(self): ...