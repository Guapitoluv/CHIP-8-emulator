from models.uintxarray import UInt16Array

class Stack:
    SIZE = 16

    def __init__(self):
        self.data = UInt16Array(self.SIZE)

    def __getitem__(self, index: int):
        return self.data[index]

    def __setitem__(self, index: int, value: int):
        self.data[index] = value