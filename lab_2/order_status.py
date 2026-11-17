from enum import Enum


class OrderStatus(Enum):
    Pending = 0
    Paid = 1
    Shipped = 2
    Delivered = 3
    Cancelled = 4


# Явная таблица допустимых переходов вместо сравнения числовых значений
ALLOWED_TRANSITIONS = {
    OrderStatus.Pending: {OrderStatus.Paid, OrderStatus.Cancelled},
    OrderStatus.Paid: {OrderStatus.Shipped, OrderStatus.Cancelled},
    OrderStatus.Shipped: {OrderStatus.Delivered, OrderStatus.Cancelled},
    OrderStatus.Delivered: set(),
    OrderStatus.Cancelled: set(),
}


def status_to_string(s: OrderStatus) -> str:
    return {
        OrderStatus.Pending: "Ожидает оплаты",
        OrderStatus.Paid: "Оплачен",
        OrderStatus.Shipped: "Отправлен",
        OrderStatus.Delivered: "Доставлен",
        OrderStatus.Cancelled: "Отменён",
    }.get(s, "?")
