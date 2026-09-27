#pragma once
#include <string>
#include <memory>
#include "Electronics.h"
#include "Clothing.h"
#include "Food.h"

class ProductFactory {
public:
    virtual std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) = 0;
    virtual ~ProductFactory() = default;
};

class SmartphoneFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};

class LaptopFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};

class TShirtFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};

class JacketFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};

class MilkFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};

class BreadFactory : public ProductFactory {
public:
    std::unique_ptr<Product> createProduct(const std::string& name, int price, int qty, double weight) override;
};
