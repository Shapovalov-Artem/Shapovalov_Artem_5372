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
        self._orders: list[Order] = []
        self._customers: dict[int, Customer] = {}
        self._active_orders: dict[int, int] = {}

    def __del__(self):
        for o in self._orders: o.unsubscribe(self)

    def create_order(self, customer: Customer, items: list[Product]) -> Order:
        if customer is None: raise ValueError("Не указан клиент")
        if self._active_orders.get(customer.id, 0) >= self._max_active_orders:
            raise RuntimeError(f"У клиента «{customer.name}» уже максимум активных заказов ({self._max_active_orders})")
        order = Order(len(self._orders) + 1, customer)
        for item in items: order.add_item(item.clone())
        order.subscribe(self)
        self._customers[customer.id] = customer
        self._active_orders[customer.id] = self._active_orders.get(customer.id, 0) + 1
        self._orders.append(order)
        return order

    def get_order(self, order_id: int) -> Order:
        if order_id < 1 or order_id > len(self._orders): raise IndexError("Заказ не найден")
        return self._orders[order_id - 1]

    def update_status(self, order_id: int, new_status: OrderStatus):
        self.get_order(order_id).set_status(new_status)

    @property
    def turnover(self): return self._turnover
    @property
    def customer_count(self): return len(self._customers)

    def on_order_event(self, event: OrderEvent):
        order = self.get_order(event.order_id)
        print(f"  [OrderManager] заказ #{order.id}: "
              f"{status_to_string(event.old_status)} -> {status_to_string(event.new_status)}")
        if event.new_status == OrderStatus.Paid:
            self._turnover += order.total_price
            order.customer.add_bonus(order.cashback)
        elif event.new_status in (OrderStatus.Cancelled, OrderStatus.Delivered):
            self._active_orders[order.customer.id] -= 1