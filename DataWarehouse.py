

class DataWarehouse:
    """ basic stack implementation used from prior projects """
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.next = None


    def __init__(self):
        self.top = None
        self.size = 0


    def is_empty(self):
        return self.size == 0


    def push(self, data):
        if data is not None:
            n = DataWarehouse.Node(data)
            if self.is_empty():
                self.top = n
            else:
                n.next = self.top
                self.top = n

            self.size += 1


    def pop(self):
        if self.is_empty():
            return None
        else:
            r = self.top
            self.top = self.top.next

        self.size -= 1
        return r.data


    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.top.data



