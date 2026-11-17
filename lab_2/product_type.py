class ProductType:
    _pool: dict = {}

    def __init__(self, category: str, base_weight: float, base_price: float):
        self._category = category
        self._base_weight = base_weight
        self._base_price = base_price

    @classmethod
    def _init_pool(cls):
        if cls._pool:
            return

        def add(c, w, p):
            cls._pool[c] = ProductType(c, w, p)

        add("milk", 1.0, 90.0)
        add("bread", 0.4, 50.0)
        add("cheese", 0.5, 450.0)
        add("water", 6.0, 120.0)
        add("mug", 0.3, 250.0)
        add("Electronics", 0.5, 500.0)
        add("Clothing", 0.3, 100.0)
        add("Food", 1.0, 100.0)

    @classmethod
    def get_type(cls, category: str) -> "ProductType":
        cls._init_pool()
        if category not in cls._pool:
            raise KeyError(f"Неизвестная категория: {category}")
        return cls._pool[category]

    @classmethod
    def pool_size(cls) -> int:
        cls._init_pool()
        return len(cls._pool)

    @property
    def category(self): return self._category
    @property
    def base_weight(self): return self._base_weight
    @property
    def base_price(self): return self._base_price
