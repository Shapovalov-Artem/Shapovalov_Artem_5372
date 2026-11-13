# order_status.py
from enum import Enum

class OrderStatus(Enum):
    Pending = 0
    Paid = 1
    Shipped = 2
    Delivered = 3
    Cancelled = 4

def status_to_string(s: OrderStatus) -> str:
    return {
        OrderStatus.Pending: "Ожидает оплаты",
        OrderStatus.Paid: "Оплачен",
        OrderStatus.Shipped: "Отправлен",
        OrderStatus.Delivered: "Доставлен",
        OrderStatus.Cancelled: "Отменён",
    }.get(s, "?")