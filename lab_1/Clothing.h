#pragma once
#include "Product.h"

class Clothing : public Product {
public:
    using Product::Product;
};

class TShirt : public Clothing {
public:
    TShirt(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};

class Jacket : public Clothing {
public:
    Jacket(std::string name, int price, int qty, double weight);
    std::unique_ptr<Product> clone() const override;
};
