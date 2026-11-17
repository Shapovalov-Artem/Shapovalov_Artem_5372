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
    check("У товара из фабрики есть тип из пула", p.type is ProductType.get_type("Electronics"))
    check("clone сохраняет класс товара", isinstance(p.clone(), Smartphone))

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
    moved = original.move()
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

    # отмена оплаченного заказа откатывает оборот и бонусы
    manager.update_status(o.id, OrderStatus.Cancelled)
    check("Отмена оплаченного откатывает оборот", abs(manager.turnover) < 1e-6)
    check("Отмена оплаченного откатывает бонусы", abs(ivan.bonus) < 1e-6)
    o_next = manager.create_order(ivan, [item(1, 1, "milk")])
    check("После отмены лимит активных освобождён", o_next.id == 2)
    threw = False
    try: manager.update_status(o.id, OrderStatus.Cancelled)
    except RuntimeError: threw = True
    check("Повторная отмена запрещена", threw)
    threw = False
    try: manager.create_order(ivan, [item(1, 1, "milk")])
    except RuntimeError: threw = True
    check("Счётчик активных не ушёл в минус (лимит держится)", threw)

    # операторы
    petr = Customer(2, "П", "Москва")
    big = manager.create_order(petr, [item(1, 5, "milk"), item(2, 1, "bread")])
    check("Оператор >: большой заказ дороже", big > o_next)
    check("Оператор <: малый заказ дешевле", o_next < big)
    big - 2
    check("Оператор -: позиция удалена", len(big.items) == 1)
    threw = False
    try: big - 999
    except ValueError: threw = True
    check("Оператор -: неизвестный товар даёт ошибку", threw)

    # прокси: запасной способ
    far = manager.create_order(Customer(3, "З", "Владивосток"), [item(1, 1, "milk")])
    far << DeliveryProxy(CourierDelivery(), ["Москва"], 50.0, fallback=PickupDelivery())
    check("Прокси переключился на самовывоз", far.get_delivery_cost() == 0.0)
    far2 = manager.create_order(Customer(4, "Я", "Владивосток"), [item(1, 1, "milk")])
    threw = False
    try: far2 << DeliveryProxy(CourierDelivery(), ["Москва"], 50.0)
    except ValueError: threw = True
    check("Прокси без запасного способа отказывает", threw)

    # delivery << order, NotImplemented, get_items, отписка
    o5 = manager.create_order(Customer(5, "К", "Москва"), [item(1, 1, "milk")])
    pickup = PickupDelivery()
    check("get_estimated_time() работает без аргументов", pickup.get_estimated_time() == "1-3 дня")
    res = pickup << o5
    check("Оператор delivery << order назначает доставку", res is o5 and o5.delivery is pickup)
    for label, op in [("+", lambda: o5 + 5), ("-", lambda: o5 - "x"), ("<<", lambda: o5 << 5),
                      ("delivery <<", lambda: pickup << 5)]:
        try: op(); ok = False
        except TypeError: ok = True
        check(f"Оператор {label}: неподдерживаемый тип даёт TypeError (NotImplemented)", ok)
    check("get_items возвращает неизменяемый tuple", isinstance(o5.get_items(), tuple))
    check("Именованные get_turnover/get_customer_count",
          manager.get_turnover() == manager.turnover and
          manager.get_customer_count() == manager.customer_count)
    before = manager.turnover
    o5.unsubscribe(manager)
    manager.update_status(o5.id, OrderStatus.Paid)
    check("После unsubscribe менеджер не получает события", manager.turnover == before)

    manager.close()
    print(f"\nИтого: {passed}/{total} тестов пройдено.")