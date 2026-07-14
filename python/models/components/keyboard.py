from models.uintxarray import UInt8Array


class Keyboard:
    def __init__(self):
        self.reset()
        self.valid = UInt8Array(range(0, 16))
    
    def reset(self) -> None:
        self.keys = UInt8Array(16)
        self.last_pressed = None
    
    def validate(self, key: int) -> bool:
        if key not in self.valid:
            raise ValueError("Invalid key")

    def press(self, key: int) -> None:
        self.validate(key)
        self.keys[key] = 1
        self.last_pressed = key

    def release(self, key: int) -> None:
        self.validate(key)
        self.keys[key] = 0

    def is_pressed(self, key: int):
        self.validate(key)
        return bool(self.keys[key])
    
    def get_key(self):
        key = self.last_pressed
        self.last_pressed = None
        return key