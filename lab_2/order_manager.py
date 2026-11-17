import itertools
from io_observer import IObserver
from order import Order
from order_event import OrderEvent
from order_status import OrderStatus, status_to_string
from customer import Customer
from product import Product


class OrderManager(IObserver):
    def __init__(self, max_active_orders: int = 5):
        self._max_active_orders = max_active_orders
        self._turnover = 0.0
        self._orders: dict[int, Order] = {}
        self._order_ids = itertools.count(1)
        self._customers: dict[int, Customer] = {}
        self._active_orders: dict[int, int] = {} # id и число активных заказов
        self._active_ids: set[int] = set()
        self._paid: dict[int, tuple[float, float]] = {}  # id, сумма оплаты и начисленные бонусы

    def close(self):
        for o in self._orders.values():
            o.unsubscribe(self)

    def __enter__(self): return self
    def __exit__(self, *exc): self.close()

    def create_order(self, customer: Customer, items: list[Product]) -> Order:
        if customer is None: raise ValueError("Не указан клиент")
        if self._active_orders.get(customer.id, 0) >= self._max_active_orders:
            raise RuntimeError(f"У клиента «{customer.name}» уже максимум активных заказов "
                               f"({self._max_active_orders})")
        order = Order(next(self._order_ids), customer)
        for item in items: order.add_item(item.clone())
        order.subscribe(self)
        self._customers[customer.id] = customer
        self._active_orders[customer.id] = self._active_orders.get(customer.id, 0) + 1
        self._active_ids.add(order.id)
        self._orders[order.id] = order
        return order

    def get_order(self, order_id: int) -> Order:
        if order_id not in self._orders: raise IndexError("Заказ не найден")
        return self._orders[order_id]

    def update_status(self, order_id: int, new_status: OrderStatus):
        self.get_order(order_id).set_status(new_status)

    @property
    def turnover(self): return self._turnover
    @property
    def customer_count(self): return len(self._customers)

    def get_turnover(self): return self._turnover
    def get_customer_count(self): return len(self._customers)

    def _release(self, order: Order):
        """Снять заказ с учёта активных ровно один раз."""
        if order.id in self._active_ids:
            self._active_ids.discard(order.id)
            cid = order.customer.id
            self._active_orders[cid] = max(0, self._active_orders.get(cid, 0) - 1)

    def on_order_event(self, event: OrderEvent):
        order = self.get_order(event.order_id)
        print(f"  [OrderManager] заказ #{order.id}: "
              f"{status_to_string(event.old_status)} -> {status_to_string(event.new_status)}")
        if event.new_status == OrderStatus.Paid:
            amount, bonus = order.total_price, order.cashback
            self._paid[order.id] = (amount, bonus)
            self._turnover += amount
            order.customer.add_bonus(bonus)
        elif event.new_status == OrderStatus.Cancelled:
            paid = self._paid.pop(order.id, None)
            if paid is not None:
                amount, bonus = paid
                self._turnover -= amount
                order.customer.add_bonus(-bonus)
            self._release(order)
        elif event.new_status == OrderStatus.Delivered:
            self._release(order)
