#include "Food.h"

Milk::Milk(std::string name, int price, int qty, double weight)
    : Food(std::move(name), price, qty, weight, "Food") {}

std::unique_ptr<Product> Milk::clone() const {
    return std::make_unique<Milk>(*this);
}

Bread::Bread(std::string name, int price, int qty, double weight)
    : Food(std::move(name), price, qty, weight, "Food") {}

std::unique_ptr<Product> Bread::clone() const {
    return std::make_unique<Bread>(*this);
}
