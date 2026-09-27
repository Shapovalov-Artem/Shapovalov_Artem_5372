#include "Product.h"
#include <stdexcept>

int Product::nextId = 1;

Product::Product(std::string name, int price, int qty, double weight, std::string category)
    : id(nextId++),
      name(std::move(name)),
      price(price),
      quantity(qty),
      weight(weight),
      category(std::move(category)) {}

int Product::getId() const { return id; }
const std::string& Product::getName() const { return name; }
const std::string& Product::getCategory() const { return category; }
int Product::getPriceValue() const { return price.getValue(); }
int Product::getQuantityValue() const { return quantity.getValue(); }
double Product::getWeightValue() const { return weight.getValue(); }

void Product::changeQuantity(int delta) {
    int current = quantity.getValue();
    if (current + delta < 0) {
        throw std::invalid_argument("Resulting quantity can't be negative");
    }
    quantity.setValue(current + delta);
}

void Product::setPrice(const Price& newPrice) {
    price = newPrice;
}
