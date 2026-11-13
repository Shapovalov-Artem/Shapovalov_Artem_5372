import copy
from warehouse import Warehouse
from product_factory import (SmartphoneFactory, LaptopFactory, TShirtFactory,
                             JacketFactory, MilkFactory, BreadFactory)
from product import Product
from product_type import ProductType
from attributes import Price, Quantity, Weight
from customer import Customer
from order_manager import OrderManager
from order_status import OrderStatus
from delivery import CourierDelivery, PickupDelivery, PostDelivery
from delivery_proxy import DeliveryProxy
from discount import PercentDiscount, CashbackDiscount, FreeDeliveryDiscount, GiftDiscount



def print_warehouse(warehouse: Warehouse, title: str):
    print(f"--- {title} ---")
    for p in warehouse:
        print(f"  id={p.id} {p.name} ({p.category}) price={p.price_value} "
              f"qty={p.quantity_value} weight={p.weight_value}")
    if len(warehouse) == 0:
        print("  (пусто)")


def item(id: int, quantity: int, category: str) -> Product:
    return Product(id, quantity, ProductType.get_type(category))


def header(title: str):
    print(f"\n===== {title} =====")


def scenario_warehouse():
    header("Склад: добавление товаров всеми фабриками")
    wh = Warehouse(6)
    wh.add_product(SmartphoneFactory().create_product("iPhone 15", 999, 10, 0.19))
    wh.add_product(LaptopFactory().create_product("MacBook Air", 1299, 5, 1.24))
    wh.add_product(TShirtFactory().create_product("Basic Tee", 25, 50, 0.2))
    wh.add_product(JacketFactory().create_product("Winter Jacket", 150, 20, 0.9))
    wh.add_product(MilkFactory().create_product("Milk 1L", 2, 100, 1.0))
    wh.add_product(BreadFactory().create_product("Bread", 1, 80, 0.4))
    print_warehouse(wh, "Склад")

    # копирование / перемещение / поиск / перенос
    copy_wh = copy.copy(wh)
    p = copy_wh.find_by_id(1)
    if p: p.change_quantity(+100)
    print_warehouse(wh, "Оригинал (не изменился)")
    print_warehouse(copy_wh, "Копия (изменена)")

    moved = wh.__move__()
    print(f"После move: source size={len(wh)}, moved size={len(moved)}")

    # перенос товара между складами
    secondary = Warehouse(3)
    moved.transfer_product(next(iter(moved)).id, secondary)
    print_warehouse(secondary, "Целевой склад после переноса")


def scenario_orders():
    ivan = Customer(1, "Иван", "Москва")
    anna = Customer(2, "Анна", "Владивосток")
    manager = OrderManager(2)

    header("Сценарий 1: создание заказа, Легковес, доставка")
    milk1 = item(1, 3, "milk")
    milk2 = item(2, 6, "milk")
    same = "да" if milk1.type is milk2.type else "нет"
    print(f"Типов в пуле: {ProductType.pool_size()}, у двух «milk» общий тип: {same}\n")

    order1 = manager.create_order(ivan, [milk1, item(3, 2, "bread"), item(4, 1, "cheese")])
    courier = CourierDelivery()
    order1 << courier
    print(order1)

    header("Сценарий 2: акции и уведомления")
    order1 + PercentDiscount() + CashbackDiscount() + FreeDeliveryDiscount() + GiftDiscount()
    print(order1)

    manager.update_status(order1.id, OrderStatus.Paid)
    print(f"Оборот: {manager.turnover:.2f}, бонусы Ивана: {ivan.bonus:.2f}, "
          f"клиентов: {manager.customer_count}")
    manager.update_status(order1.id, OrderStatus.Shipped)
    manager.update_status(order1.id, OrderStatus.Delivered)
    try:
        manager.update_status(order1.id, OrderStatus.Pending)
    except RuntimeError as e:
        print(f"Ожидаемая ошибка: {e}")

    header("Сценарий 3: прокси доставки")
    proxy = DeliveryProxy(courier, ["Москва", "Санкт-Петербург"], 50.0)
    order2 = manager.create_order(ivan, [item(1, 2, "milk")])
    order2 << proxy
    print(order2)

    order3 = manager.create_order(anna, [item(1, 1, "milk")])
    try:
        order3 << proxy
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    heavy = manager.create_order(anna, [item(1, 5, "water")])
    print(f"Вес заказа: {heavy.total_weight:.2f} кг. Курьер подходит? "
          f"{'да' if courier.is_available(heavy) else 'нет'}")
    heavy << PickupDelivery()
    print(heavy)

    header("Сценарий 4: лимит заказов и глубокое копирование")
    try:
        manager.create_order(anna, [item(1, 1, "bread")])
    except RuntimeError as e:
        print(f"Ожидаемая ошибка: {e}")
    manager.update_status(order3.id, OrderStatus.Cancelled)
    manager.create_order(anna, [item(1, 1, "bread")])
    print("Заказ создан после отмены предыдущего")

    copy_order = copy.copy(heavy)
    copy_order.add_item(item(7, 1, "cheese"))
    print(f"Позиций в копии: {len(copy_order.items)}, в оригинале: {len(heavy.items)}")


def run_tests():
    header("Тестирование")
    passed = total = 0
    def check(name, cond):
        nonlocal passed, total
        total += 1
        print(f"{'[OK]   ' if cond else '[FAIL] '}{name}")
        if cond: passed += 1

    for cls, arg, label in [(Price, -1, "Price"), (Quantity, -5, "Quantity"), (Weight, -0.5, "Weight")]:
        try: cls(arg); check(f"{label} бросает при отрицательном", False)
        except ValueError: check(f"{label} бросает при отрицательном", True)

    p = SmartphoneFactory().create_product("Test", 100, 1, 0.1)
    check("SmartphoneFactory: категория Electronics", p.category == "Electronics")
    check("SmartphoneFactory: имя", p.name == "Test")

    p = MilkFactory().create_product("Test Milk", 3, 1, 1.0)
    check("MilkFactory: категория Food", p.category == "Food")

    wh = Warehouse(3)
    wh.add_product(SmartphoneFactory().create_product("A", 10, 1, 0.1))
    wh.add_product(MilkFactory().create_product("B", 5, 1, 0.5))
    check("Итератор: 2 из 2", len(wh) == 2)

    original = Warehouse(3)
    original.add_product(SmartphoneFactory().create_product("A", 10, 5, 0.1))
    new_id = next(iter(original)).id
    cp = copy.copy(original)
    cp.find_by_id(new_id).change_quantity(+50)
    check("Глубокая копия независима",
          original.find_by_id(new_id).quantity_value == 5 and
          cp.find_by_id(new_id).quantity_value == 55)

    original = Warehouse(3)
    original.add_product(SmartphoneFactory().create_product("A", 10, 5, 0.1))
    before = next(iter(original))
    moved = original.__move__()
    check("Move сохраняет адрес", moved.find_by_id(before.id) is before)
    check("После move источник пуст", len(original) == 0)

    tiny = Warehouse(1)
    tiny.add_product(SmartphoneFactory().create_product("A", 10, 1, 0.1))
    threw = False
    try: tiny.add_product(SmartphoneFactory().create_product("B", 10, 1, 0.1))
    except OverflowError: threw = True
    check("addProduct: OverflowError при переполнении", threw)

    # заказы
    manager = OrderManager(1)
    ivan = Customer(1, "И", "Москва")
    o = manager.create_order(ivan, [item(1, 1, "milk")])
    o + PercentDiscount() + CashbackDiscount()
    check("Скидка 10% применилась", abs(o.discount_amount - 9.0) < 1e-6)
    manager.update_status(o.id, OrderStatus.Paid)
    check("Оборот вырос", manager.turnover > 0)
    check("Бонус начислен", ivan.bonus > 0)

    print(f"\nИтого: {passed}/{total} тестов пройдено.")


def main():
    scenario_warehouse()
    scenario_orders()
    run_tests()


if __name__ == "__main__":
    main()