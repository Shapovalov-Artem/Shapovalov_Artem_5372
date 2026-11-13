from delivery import Delivery

class DeliveryProxy(Delivery):
    def __init__(self, real: Delivery, allowed_regions: list[str], max_weight: float):
        self._real = real
        self._allowed_regions = list(allowed_regions)
        self._max_weight = max_weight
        self._cache: dict[tuple[str, int], float] = {}

    def get_cost(self, order):
        print(f"  [LOG] getCost(заказ #{order.id})")
        key = (order.region, round(order.total_weight * 1000))
        if key in self._cache:
            print(f"  [LOG] взято из кеша: {self._cache[key]} руб.")
            return self._cache[key]
        cost = self._real.get_cost(order)
        self._cache[key] = cost
        print(f"  [LOG] рассчитано и сохранено в кеш: {cost} руб.")
        return cost

    def get_estimated_time(self): return self._real.get_estimated_time()

    def is_available(self, order):
        print(f"  [LOG] isAvailable(заказ #{order.id})")
        if order.total_weight > self._max_weight:
            print("  [LOG] отказ: превышен вес"); return False
        if order.region not in self._allowed_regions:
            print(f"  [LOG] отказ: регион «{order.region}» не обслуживается"); return False
        return self._real.is_available(order)

    def get_name(self): return f"Прокси[{self._real.get_name()}]"