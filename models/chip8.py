from models.components.cpu import CPU
from models.components.memory import Memory
from models.components.stack import Stack
from models.components.display import Display
from models.components.keyboard import Keyboard
from models.components.timers import Timers


class Chip8:
    def __init__(self) -> None:
        self.memory: Memory = Memory()
        self.stack: Stack = Stack()
        self.display: Display = Display()
        self.keyboard: Keyboard = Keyboard()
        self.timers: Timers = Timers()

        self.cpu: CPU = CPU(
            self.memory,
            self.stack,
            self.display,
            self.keyboard,
            self.timers
        )

    def load_rom(self, rom: list[int]) -> None:
        self.memory.load(0x200, rom)

    def cycle(self) -> None:
        self.cpu.cycle()

    def run(self) -> None:
        while True:
            self.cycle()