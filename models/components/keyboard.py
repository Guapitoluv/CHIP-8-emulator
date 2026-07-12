from models.uintxarray import UInt8Array


class Keyboard:

    def __init__(self):
        self.keys = UInt8Array(16)

    def press(self, key: int):
        self.keys[key] = 1

    def release(self, key: int):
        self.keys[key] = 0

    def is_pressed(self, key: int):
        return bool(self.keys[key])