#include "Attributes.h"

Price::Price(int val) : value(val) {
    if (val < 0) {
        throw std::invalid_argument("Price can't be negative");
    }
}
int Price::getValue() const { return value; }
void Price::setValue(int newVal) {
    if (newVal < 0) {
        throw std::invalid_argument("Value can't be negative");
    }
    value = newVal;
}

Quantity::Quantity(int val) : value(val) {
    if (val < 0) {
        throw std::invalid_argument("Quantity can't be negative");
    }
}
int Quantity::getValue() const { return value; }
void Quantity::setValue(int newVal) {
    if (newVal < 0) {
        throw std::invalid_argument("Value can't be negative");
    }
    value = newVal;
}

Weight::Weight(double val) : value(val) {
    if (val < 0) {
        throw std::invalid_argument("Weight can't be negative");
    }
}
double Weight::getValue() const { return value; }
void Weight::setValue(double newVal) {
    if (newVal < 0) {
        throw std::invalid_argument("Value can't be negative");
    }
    value = newVal;
}
