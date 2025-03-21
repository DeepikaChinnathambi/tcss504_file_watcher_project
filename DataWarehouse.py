

class DataWarehouse:
    """ basic stack implementation used from prior projects """
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.next = None


    def __init__(self):
        self._top = None
        self._size = 0


    def is_empty(self):
        return self._size == 0


    def push(self, data):
        if data is not None:
            n = DataWarehouse.Node(data)
            if self.is_empty():
                self._top = n
            else:
                n.next = self._top
                self._top = n

            self._size += 1


    def pop(self):
        if self.is_empty():
            return None
        else:
            r = self._top
            self._top = self._top.next

        self._size -= 1
        return r.data


    def peek(self):
        if self.is_empty():
            return None
        else:
            return self._top.data



