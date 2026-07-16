from models.uintxarray import UInt16Array
from constants import STACK_SIZE

class Stack:
    SIZE = STACK_SIZE

    def __init__(self, registers = None):
        self.data = UInt16Array(self.SIZE)
        self.registers = registers

    def __getitem__(self, index: int):
        return self.data[index]

    def __setitem__(self, index: int, value: int):
        self.data[index] = value

    def push(self, value: int) -> None:
        self.data[self.registers.sp] = value
        self.registers.sp += 1

    def pop(self) -> int:
        self.registers.sp -= 1
        return int(self.data[self.registers.sp])

    def reset(self) -> None:
        self.registers.sp = 0