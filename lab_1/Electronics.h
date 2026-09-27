#pragma once
#include "Product.h"

class Electronics : public Product {
public:
    using Product::Product;
};

class Smartphone : public Electronics {
public:
    Smartphone(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};

class Laptop : public Electronics {
public:
    Laptop(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};
