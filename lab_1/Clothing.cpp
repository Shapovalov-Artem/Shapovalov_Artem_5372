#include "Clothing.h"

TShirt::TShirt(std::string name, int price, int qty, double weight)
    : Clothing(std::move(name), price, qty, weight, "Clothing") {}

std::unique_ptr<Product> TShirt::clone() const {
    return std::make_unique<TShirt>(*this);
}

Jacket::Jacket(std::string name, int price, int qty, double weight)
    : Clothing(std::move(name), price, qty, weight, "Clothing") {}

std::unique_ptr<Product> Jacket::clone() const {
    return std::make_unique<Jacket>(*this);
}
