from __future__ import annotations
from delivery_strategy import DeliveryStrategy


class DeliveryProxy(DeliveryStrategy):

    def __init__(self, real: DeliveryStrategy, allowed_regions: list[str], max_weight: float,
                 fallback: DeliveryStrategy | None = None):
        self._real = real
        self._fallback = fallback
        self._allowed_regions = list(allowed_regions)
        self._max_weight = max_weight
        self._cache: dict[tuple, float] = {}

    def _real_available(self, order, log: bool) -> bool:
        if order.total_weight > self._max_weight:
            if log: print("  [LOG] отказ: превышен вес")
            return False
        if order.region not in self._allowed_regions:
            if log: print(f"  [LOG] отказ: регион «{order.region}» не обслуживается")
            return False
        return self._real.is_available(order)

    def _select(self, order, log: bool = False) -> DeliveryStrategy | None:
        #Основной способ, а если он недоступен, то запасной
        if self._real_available(order, log):
            return self._real
        if self._fallback is not None and self._fallback.is_available(order):
            if log:
                print(f"  [LOG] переключение на запасной способ: {self._fallback.get_name()}")
            return self._fallback
        return None

    @staticmethod
    def _cache_key(order) -> tuple:
        return (order.id, order.region, round(order.total_weight * 1000),
                round(order.items_price * 100))

    def get_cost(self, order):
        print(f"  [LOG] getCost(заказ #{order.id})")
        key = self._cache_key(order)
        if key in self._cache:
            print(f"  [LOG] взято из кеша: {self._cache[key]} руб.")
            return self._cache[key]
        strategy = self._select(order)
        if strategy is None:
            raise ValueError("Нет доступного способа доставки")
        cost = strategy.get_cost(order)
        self._cache[key] = cost
        print(f"  [LOG] рассчитано и сохранено в кеш: {cost} руб.")
        return cost

    def get_estimated_time(self, order=None):
        if order is None:
            return self._real.get_estimated_time()
        strategy = self._select(order)
        return strategy.get_estimated_time(order) if strategy else "—"

    def is_available(self, order):
        print(f"  [LOG] isAvailable(заказ #{order.id})")
        return self._select(order, log=True) is not None

    def get_name(self):
        name = f"Прокси[{self._real.get_name()}"
        if self._fallback is not None:
            name += f" -> {self._fallback.get_name()}"
        return name + "]"
