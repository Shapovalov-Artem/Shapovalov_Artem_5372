from __future__ import annotations
from customer import Customer
from delivery_strategy import DeliveryStrategy
from discount_strategy import DiscountStrategy
from io_observable import IObservable
from io_observer import IObserver
from order_event import OrderEvent
from order_status import OrderStatus, ALLOWED_TRANSITIONS, status_to_string
from product import Product


class Order(IObservable):
    def __init__(self, id: int, customer: Customer):
        if customer is None: raise ValueError("У заказа должен быть клиент")
        self._id = id
        self._customer = customer
        self._items: list[Product] = []
        self._status = OrderStatus.Pending
        self._delivery: DeliveryStrategy | None = None
        self._discounts: list[str] = []
        self._discount_amount = 0.0
        self._cashback = 0.0
        self._free_delivery = False
        self._observers: list[IObserver] = []

    def __copy__(self):
        new = Order.__new__(Order)
        new._id = self._id
        new._customer = self._customer
        new._items = [i.clone() for i in self._items]
        new._status = self._status
        new._delivery = self._delivery
        new._discounts = list(self._discounts)
        new._discount_amount = self._discount_amount
        new._cashback = self._cashback
        new._free_delivery = self._free_delivery
        new._observers = []
        return new

    def add_item(self, item: Product):
        if item is None: raise ValueError("Пустой товар")
        self._items.append(item)

    def remove_item(self, product_id: int) -> bool:
        before = len(self._items)
        self._items = [p for p in self._items if p.id != product_id]
        return len(self._items) != before

    @property
    def items(self): return self.get_items()

    def get_items(self) -> tuple:
        """Состав заказа только для чтения; менять через add_item/remove_item."""
        return tuple(self._items)

    @property
    def total_weight(self): return sum(i.weight for i in self._items)
    @property
    def items_price(self): return sum(i.total_price for i in self._items)

    def get_delivery_cost(self):
        return self._delivery.get_cost(self) if (self._delivery and not self._free_delivery) else 0.0

    @property
    def total_price(self):
        return max(0.0, self.items_price - self._discount_amount) + self.get_delivery_cost()

    @property
    def status(self): return self._status

    def set_status(self, new_status: OrderStatus):
        if new_status not in ALLOWED_TRANSITIONS[self._status]:
            raise RuntimeError(f"Недопустимая смена статуса: "
                               f"{status_to_string(self._status)} -> {status_to_string(new_status)}")
        old = self._status
        self._status = new_status
        self.notify(OrderEvent(self._id, old, new_status))

    def apply_discount(self, discount: DiscountStrategy):
        discount.apply(self)
        self._discounts.append(discount.get_name())

    def set_delivery(self, delivery: DeliveryStrategy):
        if delivery is None: raise ValueError("Не указан способ доставки")
        if not delivery.is_available(self):
            raise ValueError(f"Доставка «{delivery.get_name()}» недоступна для этого заказа")
        self._delivery = delivery

    @property
    def delivery(self): return self._delivery

    def add_discount_amount(self, a): self._discount_amount += a
    def add_cashback(self, a): self._cashback += a
    def set_free_delivery(self, v): self._free_delivery = v

    @property
    def discount_amount(self): return self._discount_amount
    @property
    def cashback(self): return self._cashback
    @property
    def is_free_delivery(self): return self._free_delivery
    @property
    def discount_names(self): return self._discounts
    @property
    def id(self): return self._id
    @property
    def customer(self): return self._customer
    @property
    def region(self): return self._customer.region

    def subscribe(self, observer):
        if observer is not None and observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers = [o for o in self._observers if o is not observer]

    def notify(self, event):
        for o in list(self._observers):
            o.on_order_event(event)

    def __add__(self, discount: DiscountStrategy):
        """order + скидка: применить акцию."""
        if not isinstance(discount, DiscountStrategy): return NotImplemented
        self.apply_discount(discount)
        return self

    def __lshift__(self, delivery: DeliveryStrategy):
        """order << доставка: назначить способ доставки."""
        if not isinstance(delivery, DeliveryStrategy): return NotImplemented
        self.set_delivery(delivery)
        return self

    def __sub__(self, product_id: int):
        """order - id: удалить позицию заказа по id товара."""
        if not isinstance(product_id, int): return NotImplemented
        if not self.remove_item(product_id):
            raise ValueError(f"Товар #{product_id} не найден в заказе")
        return self

    def __lt__(self, other):
        """сравнение заказов по итоговой стоимости."""
        if not isinstance(other, Order): return NotImplemented
        return self.total_price < other.total_price

    def __gt__(self, other):
        if not isinstance(other, Order): return NotImplemented
        return self.total_price > other.total_price

    def __str__(self):
        delivery_cost = self.get_delivery_cost()
        total = self.total_price
        lines = [f"Заказ #{self._id} [{status_to_string(self._status)}], "
                 f"клиент: {self._customer.name} ({self.region})"]
        for item in self._items:
            lines.append(f"  - {item.category} x{item.quantity} = {item.total_price:.2f}")
        lines.append(f"  Вес: {self.total_weight:.2f} кг")
        for n in self._discounts: lines.append(f"  Акция: {n}")
        if self._delivery:
            lines.append(f"  Доставка: {self._delivery.get_name()}, "
                         f"{self._delivery.get_estimated_time(self)}, {delivery_cost:.2f} руб.")
        tail = f"  ИТОГО: {total:.2f} руб."
        if self._cashback > 0: tail += f" (cashback {self._cashback:.2f})"
        lines.append(tail)
        return "\n".join(lines) + "\n"
