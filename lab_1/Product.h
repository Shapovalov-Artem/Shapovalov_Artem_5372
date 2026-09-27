#pragma once
#include <string>
#include <memory>
#include "Attributes.h"

class Product {
private:
    int id;
    std::string name;
    Price price;
    Quantity quantity;
    Weight weight;
    std::string category;
    static int nextId;

public:
    Product(std::string name, int price, int qty, double weight, std::string category);

    Product(const Product& other) = default;
    Product& operator=(const Product&) = delete;

    virtual ~Product() = default;

    virtual std::unique_ptr<Product> clone() const = 0;

    int getId() const;
    const std::string& getName() const;
    const std::string& getCategory() const;
    int getPriceValue() const;
    int getQuantityValue() const;
    double getWeightValue() const;

    void changeQuantity(int delta);
    void setPrice(const Price& newPrice);
};
