import copy
from warehouse import Warehouse
from product_factory import (SmartphoneFactory, LaptopFactory, TShirtFactory,
                             JacketFactory, MilkFactory, BreadFactory)
from electronics import Smartphone
from product import Product
from product_type import ProductType
from price import Price
from quantity import Quantity
from weight import Weight
from customer import Customer
from order_manager import OrderManager
from order_status import OrderStatus
from courier_delivery import CourierDelivery
from pickup_delivery import PickupDelivery
from delivery_proxy import DeliveryProxy
from percent_discount import PercentDiscount
from cashback_discount import CashbackDiscount
from free_delivery_discount import FreeDeliveryDiscount
from gift_discount import GiftDiscount


def item(id: int, quantity: int, category: str) -> Product:
    return Product.from_type(id, quantity, ProductType.get_type(category))


def header(title: str):
    print(f"\n{title}")

def scenario_orders():
    ivan = Customer(1, "Иван", "Москва")
    anna = Customer(2, "Анна", "Владивосток")
    manager = OrderManager(2)

    # Считаем активные заказы среди созданных в этом сценарии.
    # Активными считаются заказы, которые ещё не доставлены и не отменены.
    scenario_orders_list = []

    def active_orders_count():
        finished = {OrderStatus.Delivered, OrderStatus.Cancelled}
        return sum(order.status not in finished for order in scenario_orders_list)

    try:
        header("Сценарий 1: создание заказа через OrderManager и процентная скидка")
        milk1 = item(1, 3, "milk")
        milk2 = item(2, 6, "milk")
        same = "да" if milk1.type is milk2.type else "нет"
        print(f"Типов в пуле: {ProductType.pool_size()}, "
              f"у двух «milk» общий тип: {same}")

        order1 = manager.create_order(
            ivan, [milk1, item(3, 2, "bread"), item(4, 1, "cheese")]
        )
        scenario_orders_list.append(order1)

        print("Заказ создан через OrderManager, товары добавлены:")
        print(order1)

        before_discount = order1.total_price
        order1 + PercentDiscount()
        print(f"После PercentDiscount: цена {before_discount:.2f} -> "
              f"{order1.total_price:.2f}; "
              f"размер скидки: {order1.discount_amount:.2f}")

        header("Сценарий 2: выбор доставки через delivery << order и DeliveryProxy")
        courier = CourierDelivery()

        # Оператор определён в DeliveryStrategy: доставка назначается заказу.
        courier << order1
        print(f"Для заказа #{order1.id} назначена доставка: "
              f"{order1.delivery.get_name()}, "
              f"стоимость: {order1.get_delivery_cost():.2f} руб.")

        proxy = DeliveryProxy(courier, ["Москва", "Санкт-Петербург"], 50.0)

        order2 = manager.create_order(ivan, [item(1, 2, "milk")])
        scenario_orders_list.append(order2)
        proxy << order2
        print(f"Для заказа #{order2.id} прокси проверил доступность: "
              f"{proxy.is_available(order2)}; "
              f"доставка: {order2.delivery.get_name()}; "
              f"стоимость: {order2.get_delivery_cost():.2f} руб.")

        order3 = manager.create_order(anna, [item(1, 1, "milk")])
        scenario_orders_list.append(order3)
        print(f"Для заказа #{order3.id} (Владивосток) доставка через прокси "
              f"доступна: {proxy.is_available(order3)}")
        try:
            proxy << order3
        except ValueError as e:
            print(f"Ожидаемый отказ при назначении доставки: {e}")

        header("Сценарий 3: смена статуса, Observer и обновление оборота")
        turnover_before = manager.turnover
        bonus_before = ivan.bonus

        manager.update_status(order1.id, OrderStatus.Paid)
        print(f"После оплаты: статус={order1.status.name}; "
              f"оборот: {turnover_before:.2f} -> {manager.turnover:.2f}; "
              f"бонус Ивана: {bonus_before:.2f} -> {ivan.bonus:.2f}")

        manager.update_status(order1.id, OrderStatus.Shipped)
        print(f"После отправки статус заказа: {order1.status.name}")

        manager.update_status(order1.id, OrderStatus.Delivered)
        print(f"После доставки статус заказа: {order1.status.name}; "
              f"активных заказов в сценарии: {active_orders_count()}")

        try:
            manager.update_status(order1.id, OrderStatus.Pending)
        except RuntimeError as e:
            print(f"Ожидаемая ошибка недопустимого перехода: {e}")

        header("Сценарий 4: применение нескольких скидок к одному заказу")
        order4 = manager.create_order(
            ivan, [item(1, 2, "milk"), item(3, 1, "bread"),
                   item(4, 1, "cheese")]
        )
        scenario_orders_list.append(order4)

        # Назначаем платную доставку, чтобы FreeDeliveryDiscount имела эффект.
        courier << order4
        base_price = order4.total_price
        print(f"Начальная цена с доставкой: {base_price:.2f} руб.")

        (order4 + PercentDiscount() + CashbackDiscount()
         + FreeDeliveryDiscount() + GiftDiscount())

        final_price = order4.total_price
        print(f"После применения скидок: {final_price:.2f} руб.")
        print(f"Общая скидка на товары: {order4.discount_amount:.2f} руб.")
        print(f"Бесплатная доставка: {'да' if order4.is_free_delivery else 'нет'}")
        print(f"Кэшбэк: {order4.cashback:.2f} руб.")
        print("Состав заказа после добавления подарка:")
        print(order4)

        assert final_price <= base_price, (
            "Итоговая цена не должна превышать начальную цену заказа"
        )

        header("Сценарий 5: отмена заказа, освобождение лимита и статистика клиентов")
        # Оплачиваем заказ, чтобы при отмене проверить откат оборота и бонуса.
        manager.update_status(order4.id, OrderStatus.Paid)
        turnover_before_cancel = manager.turnover
        bonus_before_cancel = ivan.bonus

        print(f"До отмены: активных заказов={active_orders_count()}, "
              f"клиентов={manager.customer_count}, "
              f"оборот={turnover_before_cancel:.2f} руб.")

        manager.update_status(order4.id, OrderStatus.Cancelled)

        print(f"После отмены заказа #{order4.id}: "
              f"активных заказов={active_orders_count()}, "
              f"клиентов={manager.customer_count}")
        print(f"Оборот: {turnover_before_cancel:.2f} -> "
              f"{manager.turnover:.2f} руб.")
        print(f"Бонус Ивана: {bonus_before_cancel:.2f} -> {ivan.bonus:.2f} руб.")

        assert abs(manager.turnover - (turnover_before_cancel - order4.total_price)) < 1e-6
        assert abs(ivan.bonus - (bonus_before_cancel - order4.cashback)) < 1e-6

        # Лимит задан на одного клиента: после отмены Иван может создать новый заказ.
        new_order = manager.create_order(ivan, [item(1, 1, "bread")])
        scenario_orders_list.append(new_order)
        print(f"Новый заказ Ивана создан: id={new_order.id}; "
              f"активных заказов в сценарии={active_orders_count()}; "
              f"клиентов в статистике={manager.customer_count}")

        try:
            manager.update_status(order4.id, OrderStatus.Cancelled)
        except RuntimeError as e:
            print(f"Ожидаемая ошибка повторной отмены: {e}")

    finally:
        manager.close()


def main():
    scenario_orders()


if __name__ == "__main__":
    main()
