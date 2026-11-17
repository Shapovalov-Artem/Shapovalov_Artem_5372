import time


class OrderEvent:
    def __init__(self, order_id, old_status, new_status):
        self._order_id = order_id
        self._old_status = old_status
        self._new_status = new_status
        self._timestamp = time.time()

    @property
    def order_id(self): return self._order_id
    @property
    def old_status(self): return self._old_status
    @property
    def new_status(self): return self._new_status
    @property
    def timestamp(self): return self._timestamp
