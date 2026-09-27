#pragma once
#include <vector>
#include <memory>
#include <cstddef>
#include "Product.h"

class Warehouse {
private:
    std::vector<std::unique_ptr<Product>> products_;
    size_t maxSize_;

public:
    using iterator = std::vector<std::unique_ptr<Product>>::iterator;
    using const_iterator = std::vector<std::unique_ptr<Product>>::const_iterator;

    explicit Warehouse(size_t maxSize);

    Warehouse(const Warehouse& other);
    Warehouse& operator=(const Warehouse& other);

    Warehouse(Warehouse&& other) noexcept;
    Warehouse& operator=(Warehouse&& other) noexcept;

    ~Warehouse() = default;

    void addProduct(std::unique_ptr<Product> product);
    bool transferProduct(int productId, Warehouse& targetWarehouse);
    void removeById(int id);
    void removeByIndex(size_t index);
    Product* findById(int id);
    size_t size() const;

    iterator begin();
    iterator end();
    const_iterator begin() const;
    const_iterator end() const;
    const_iterator cbegin() const;
    const_iterator cend() const;
};
