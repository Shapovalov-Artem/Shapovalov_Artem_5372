class Price:
    def __init__(self, val: int):
        if val < 0:
            raise ValueError("Price can't be negative")
        self._value = val

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_val: int):
        if new_val < 0:
            raise ValueError("Value can't be negative")
        self._value = new_val
