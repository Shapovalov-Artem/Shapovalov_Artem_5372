from abc import ABC, abstractmethod
from product import Product
from electronics import Smartphone, Laptop
from clothing import TShirt, Jacket
from food import Milk, Bread


class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name, price, qty, weight) -> Product: ...


class SmartphoneFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return Smartphone(name, price, qty, weight)
class LaptopFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return Laptop(name, price, qty, weight)
class TShirtFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return TShirt(name, price, qty, weight)
class JacketFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return Jacket(name, price, qty, weight)
class MilkFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return Milk(name, price, qty, weight)
class BreadFactory(ProductFactory):
    def create_product(self, name, price, qty, weight): return Bread(name, price, qty, weight)