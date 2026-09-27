#pragma once
#include "Product.h"

class Food : public Product {
public:
    using Product::Product;
};

class Milk : public Food {
public:
    Milk(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};

class Bread : public Food {
public:
    Bread(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};
