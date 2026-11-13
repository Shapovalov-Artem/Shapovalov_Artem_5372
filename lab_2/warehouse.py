from __future__ import annotations
from product import Product


class Warehouse:
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise ValueError("Size must be greater than zero")
        self._products: list[Product] = []
        self._max_size = max_size

    def __copy__(self):
        new = Warehouse.__new__(Warehouse)
        new._max_size = self._max_size
        new._products = [p.clone() for p in self._products]
        return new

    def __move__(self):
        new = Warehouse.__new__(Warehouse)
        new._products = self._products
        new._max_size = self._max_size
        self._products = []
        self._max_size = 0
        return new

    def __iter__(self): return iter(self._products)
    def __len__(self): return len(self._products)
    def size(self): return len(self._products)
    def is_full(self): return len(self._products) >= self._max_size

    def add_product(self, product: Product):
        if product is None: raise ValueError("Cannot add null product")
        if len(self._products) >= self._max_size: raise OverflowError("Warehouse is full")
        self._products.append(product)

    def transfer_product(self, product_id: int, target: "Warehouse") -> bool:
        if product_id <= 0: raise ValueError("Id must be positive")
        if self is target or target.is_full(): return False
        for i, p in enumerate(self._products):
            if p is not None and p.id == product_id:
                target.add_product(p)
                del self._products[i]
                return True
        return False

    def remove_by_id(self, id_: int):
        if id_ <= 0: raise ValueError("Id must be positive")
        self._products = [p for p in self._products if p is None or p.id != id_]

    def remove_by_index(self, index: int):
        if index < 0 or index >= len(self._products): raise IndexError("Index out of range")
        del self._products[index]

    def find_by_id(self, id_: int) -> Product | None:
        if id_ <= 0: raise ValueError("Id must be positive")
        for p in self._products:
            if p is not None and p.id == id_: return p
        return None