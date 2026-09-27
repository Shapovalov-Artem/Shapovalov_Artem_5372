#include <iostream>
#include <cassert>
#include <string>
#include "Warehouse.h"
#include "ProductFactory.h"

void printWarehouse(const Warehouse& warehouse, const std::string& title) {
    std::cout << "--- " << title << " ---\n";
    for (const auto& product : warehouse) {
        std::cout << "  id=" << product->getId()
                   << " " << product->getName()
                   << " (" << product->getCategory() << ")"
                   << " price=" << product->getPriceValue()
                   << " qty=" << product->getQuantityValue()
                   << " weight=" << product->getWeightValue() << "\n";
    }
    if (warehouse.size() == 0) {
        std::cout << "  (пусто)\n";
    }
}

Warehouse scenario1() {
    std::cout << "\n========== Сценарий 1 ==========\n";
    Warehouse warehouse(6);

    SmartphoneFactory smartphoneFactory;
    LaptopFactory laptopFactory;
    TShirtFactory tshirtFactory;
    JacketFactory jacketFactory;
    MilkFactory milkFactory;
    BreadFactory breadFactory;

    warehouse.addProduct(smartphoneFactory.createProduct("iPhone 15", 999, 10, 0.19));
    warehouse.addProduct(laptopFactory.createProduct("MacBook Air", 1299, 5, 1.24));
    warehouse.addProduct(tshirtFactory.createProduct("Basic Tee", 25, 50, 0.2));
    warehouse.addProduct(jacketFactory.createProduct("Winter Jacket", 150, 20, 0.9));
    warehouse.addProduct(milkFactory.createProduct("Milk 1L", 2, 100, 1.0));
    warehouse.addProduct(breadFactory.createProduct("Bread", 1, 80, 0.4));

    printWarehouse(warehouse, "Склад после добавления товаров всеми фабриками");
    return warehouse;
}

void scenario2(const Warehouse& original) {
    std::cout << "\n========== Сценарий 2 ==========\n";
    Warehouse copy = original;

    if (Product* p = copy.findById(1)) {
        p->changeQuantity(+100);
        p->setPrice(Price(1));
    }

    printWarehouse(original, "Оригинал (не должен был измениться)");
    printWarehouse(copy, "Копия (изменена)");

    const Product* origProduct = nullptr;
    for (const auto& item : original) {
        if (item->getId() == 1) { origProduct = item.get(); break; }
    }
    assert(origProduct != nullptr && origProduct->getQuantityValue() == 10
           && "Оригинал не должен был измениться после правки копии");
    std::cout << "Проверка пройдена: изменение копии не затронуло оригинал.\n";
}

void scenario3() {
    std::cout << "\n========== Сценарий 3 ==========\n";
    Warehouse source(2);
    SmartphoneFactory smartphoneFactory;
    source.addProduct(smartphoneFactory.createProduct("Pixel 9", 799, 3, 0.18));

    Product* beforeMove = source.findById(source.begin()->get()->getId());
    size_t sizeBeforeMove = source.size();

    Warehouse moved = std::move(source);

    Product* afterMove = moved.findById(beforeMove->getId());

    std::cout << "Размер source до move: " << sizeBeforeMove << "\n";
    std::cout << "Размер source после move: " << source.size() << "\n";
    std::cout << "Размер moved после move: " << moved.size() << "\n";

    assert(afterMove != nullptr && afterMove == beforeMove
           && "После move адрес товара должен остаться тем же (без копирования)");
    assert(source.size() == 0 && "После move источник должен быть пуст");
    std::cout << "Проверка пройдена: перемещение не копировало объекты Product.\n";
}

void scenario4(Warehouse& warehouse) {
    std::cout << "\n========== Сценарий 4 ==========\n";

    if (Product* p = warehouse.findById(3)) {
        std::cout << "findById(3): " << p->getName() << "\n";
    }

    warehouse.removeById(5);
    std::cout << "После removeById(5):\n";
    printWarehouse(warehouse, "Склад");

    if (warehouse.size() > 0) {
        warehouse.removeByIndex(0);
        std::cout << "После removeByIndex(0):\n";
        printWarehouse(warehouse, "Склад");
    }
}

void scenario5(Warehouse& warehouse) {
    std::cout << "\n========== Сценарий 5 ==========\n";
    Warehouse secondary(3);

    int idToTransfer = warehouse.begin()->get()->getId();
    bool moved = warehouse.transferProduct(idToTransfer, secondary);
    std::cout << "Перенос товара id=" << idToTransfer << ": "
              << (moved ? "успешно" : "не удалось") << "\n";

    if (Product* p = secondary.findById(idToTransfer)) {
        p->changeQuantity(-2);
        p->setPrice(Price(p->getPriceValue() + 10));
        std::cout << "После изменения на новом складе: qty=" << p->getQuantityValue()
                   << " price=" << p->getPriceValue() << "\n";
    }

    printWarehouse(warehouse, "Исходный склад после переноса");
    printWarehouse(secondary, "Целевой склад после переноса");
}

void runTests() {
    std::cout << "\n========== Тестирование ==========\n";
    int passed = 0;
    int total = 0;

    auto check = [&](const std::string& name, bool condition) {
        ++total;
        std::cout << (condition ? "[OK]   " : "[FAIL] ") << name << "\n";
        if (condition) ++passed;
    };

    try {
        Price bad(-1);
        check("Price бросает исключение при отрицательном значении", false);
    } catch (const std::invalid_argument&) {
        check("Price бросает исключение при отрицательном значении", true);
    }

    try {
        Quantity bad(-5);
        check("Quantity бросает исключение при отрицательном значении", false);
    } catch (const std::invalid_argument&) {
        check("Quantity бросает исключение при отрицательном значении", true);
    }

    try {
        Weight bad(-0.5);
        check("Weight бросает исключение при отрицательном значении", false);
    } catch (const std::invalid_argument&) {
        check("Weight бросает исключение при отрицательном значении", true);
    }

    {
        SmartphoneFactory factory;
        auto product = factory.createProduct("Test Phone", 100, 1, 0.1);
        check("SmartphoneFactory создаёт товар категории Electronics",
              product->getCategory() == "Electronics");
        check("SmartphoneFactory сохраняет переданное имя",
              product->getName() == "Test Phone");
    }
    {
        MilkFactory factory;
        auto product = factory.createProduct("Test Milk", 3, 1, 1.0);
        check("MilkFactory создаёт товар категории Food",
              product->getCategory() == "Food");
    }

    {
        Warehouse warehouse(5);
        SmartphoneFactory sf;
        MilkFactory mf;
        warehouse.addProduct(sf.createProduct("A", 10, 1, 0.1));
        warehouse.addProduct(mf.createProduct("B", 5, 1, 0.5));
        warehouse.addProduct(mf.createProduct("C", 5, 1, 0.5));

        size_t count = 0;
        for (const auto& item : warehouse) {
            (void)item;
            ++count;
        }
        check("Итератор проходит по всем добавленным товарам (3 из 3)", count == 3);
    }

    {
        Warehouse original(3);
        SmartphoneFactory sf;
        original.addProduct(sf.createProduct("A", 10, 5, 0.1));
        int newId = original.begin()->get()->getId();

        Warehouse copy = original;
        Product* copyProduct = copy.findById(newId);
        Product* originalProduct = original.findById(newId);

        bool foundBoth = copyProduct != nullptr && originalProduct != nullptr;
        if (foundBoth) {
            copyProduct->changeQuantity(+50);
        }

        bool independent = foundBoth
                            && originalProduct->getQuantityValue() == 5
                            && copyProduct->getQuantityValue() == 55;
        check("Копирующий конструктор делает глубокую независимую копию", independent);
    }

    {
        Warehouse original(3);
        SmartphoneFactory sf;
        original.addProduct(sf.createProduct("A", 10, 5, 0.1));
        int newId = original.begin()->get()->getId();
        Product* before = original.findById(newId);

        Warehouse moved = std::move(original);
        bool sameAddress = before != nullptr && moved.findById(newId) == before;
        bool sourceEmpty = original.size() == 0;
        check("Перемещение сохраняет адрес объекта (без копирования)", sameAddress);
        check("После перемещения исходный склад пуст", sourceEmpty);
    }

    {
        Warehouse tiny(1);
        SmartphoneFactory sf;
        tiny.addProduct(sf.createProduct("A", 10, 1, 0.1));
        bool threw = false;
        try {
            tiny.addProduct(sf.createProduct("B", 10, 1, 0.1));
        } catch (const std::overflow_error&) {
            threw = true;
        }
        check("addProduct бросает overflow_error при превышении лимита", threw);
    }

    std::cout << "\nИтого: " << passed << "/" << total << " тестов пройдено.\n";
}

int main() {
    Warehouse main1 = scenario1();
    scenario2(main1);
    scenario3();
    scenario4(main1);
    scenario5(main1);
    runTests();
    return 0;
}