from models.uintxarray import UInt8Array

class Memory:
    SIZE = 4096

    def __init__(self):
        self.data = UInt8Array(self.SIZE)

    def __getitem__(self, address: int):
        return self.data[address]

    def __setitem__(self, address: int, value: int):
        self.data[address] = value

    def load(self, start_address: int, data):
        for offset, byte in enumerate(data):
            self[start_address + offset] = byte