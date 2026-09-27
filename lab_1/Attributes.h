#pragma once
#include <stdexcept>

class Price {
    int value;
public:
    explicit Price(int val);
    int getValue() const;
    void setValue(int newVal);
};

class Quantity {
    int value;
public:
    explicit Quantity(int val);
    int getValue() const;
    void setValue(int newVal);
};

class Weight {
    double value;
public:
    explicit Weight(double val);
    double getValue() const;
    void setValue(double newVal);
};
