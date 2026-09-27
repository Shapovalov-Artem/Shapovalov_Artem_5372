#include "Warehouse.h"
#include <stdexcept>

Warehouse::Warehouse(size_t maxSize) : maxSize_(maxSize) {
    if (maxSize == 0) {
        throw std::invalid_argument("Size must be greater than zero");
    }
}

Warehouse::Warehouse(const Warehouse& other) : maxSize_(other.maxSize_) {
    products_.reserve(other.products_.size());
    for (const auto& item : other.products_) {
        products_.push_back(item->clone());
    }
}

Warehouse& Warehouse::operator=(const Warehouse& other) {
    if (this != &other) {
        Warehouse temp(other);
        std::swap(this->maxSize_, temp.maxSize_);
        std::swap(this->products_, temp.products_);
    }
    return *this;
}

Warehouse::Warehouse(Warehouse&& other) noexcept
    : products_(std::move(other.products_)), maxSize_(other.maxSize_) {
    other.maxSize_ = 0;
}

Warehouse& Warehouse::operator=(Warehouse&& other) noexcept {
    if (this != &other) {
        products_ = std::move(other.products_);
        maxSize_ = other.maxSize_;
        other.maxSize_ = 0;
    }
    return *this;
}

void Warehouse::addProduct(std::unique_ptr<Product> product) {
    if (!product) {
        throw std::invalid_argument("Cannot add null product");
    }
    if (products_.size() >= maxSize_) {
        throw std::overflow_error("Warehouse is full");
    }
    products_.push_back(std::move(product));
}

// было принято перенести метод transferTo в класс Warehouse, так как это не нарушает принципы ооп
bool Warehouse::transferProduct(int productId, Warehouse& targetWarehouse) {
    if (productId <= 0) {
        throw std::invalid_argument("Id must be positive");
    }
    if (this == &targetWarehouse) {
        return false;
    }

    for (auto it = products_.begin(); it != products_.end(); ++it) {
        if (*it && (*it)->getId() == productId) {
            std::unique_ptr<Product> product = std::move(*it);
            products_.erase(it);

            try {
                targetWarehouse.addProduct(std::move(product));
                return true;
            } catch (const std::overflow_error&) {
                products_.push_back(std::move(product));
                return false;
            }
        }
    }
    return false;
}

void Warehouse::removeById(int id) {
    if (id <= 0) {
        throw std::invalid_argument("Id must be positive");
    }
    auto it = products_.begin();
    while (it != products_.end()) {
        if (*it && (*it)->getId() == id) {
            it = products_.erase(it);
        } else {
            ++it;
        }
    }
}

void Warehouse::removeByIndex(size_t index) {
    if (index >= products_.size()) {
        throw std::out_of_range("Index out of range");
    }
    products_.erase(products_.begin() + index);
}

Product* Warehouse::findById(int id) {
    if (id <= 0) {
        throw std::invalid_argument("Id must be positive");
    }
    auto it = products_.begin();
    while (it != products_.end()) {
        if (*it && (*it)->getId() == id) {
            return it->get();
        }
        ++it;
    }
    return nullptr;
}

size_t Warehouse::size() const {
    return products_.size();
}

Warehouse::iterator Warehouse::begin() { return products_.begin(); }
Warehouse::iterator Warehouse::end() { return products_.end(); }
Warehouse::const_iterator Warehouse::begin() const { return products_.begin(); }
Warehouse::const_iterator Warehouse::end() const { return products_.end(); }
Warehouse::const_iterator Warehouse::cbegin() const { return products_.cbegin(); }
Warehouse::const_iterator Warehouse::cend() const { return products_.cend(); }
