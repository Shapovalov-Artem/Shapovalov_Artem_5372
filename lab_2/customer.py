class Customer:
    def __init__(self, id: int, name: str, region: str):
        self._id, self._name, self._region = id, name, region
        self._bonus = 0.0

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def region(self): return self._region
    @property
    def bonus(self): return self._bonus

    def add_bonus(self, amount): self._bonus += amount
