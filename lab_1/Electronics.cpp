#include "Electronics.h"

Smartphone::Smartphone(std::string name, int price, int qty, double weight)
    : Electronics(std::move(name), price, qty, weight, "Electronics") {}

std::unique_ptr<Product> Smartphone::clone() const {
    return std::make_unique<Smartphone>(*this);
}

Laptop::Laptop(std::string name, int price, int qty, double weight)
    : Electronics(std::move(name), price, qty, weight, "Electronics") {}

std::unique_ptr<Product> Laptop::clone() const {
    return std::make_unique<Laptop>(*this);
}
