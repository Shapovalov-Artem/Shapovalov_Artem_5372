#include "ProductFactory.h"

std::unique_ptr<Product> SmartphoneFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<Smartphone>(name, price, qty, weight);
}

std::unique_ptr<Product> LaptopFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<Laptop>(name, price, qty, weight);
}

std::unique_ptr<Product> TShirtFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<TShirt>(name, price, qty, weight);
}

std::unique_ptr<Product> JacketFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<Jacket>(name, price, qty, weight);
}

std::unique_ptr<Product> MilkFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<Milk>(name, price, qty, weight);
}

std::unique_ptr<Product> BreadFactory::createProduct(const std::string& name, int price, int qty, double weight) {
    return std::make_unique<Bread>(name, price, qty, weight);
}
