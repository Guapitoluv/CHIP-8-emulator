from models.components.cpu import CPU
from models.components.memory import Memory
from models.components.stack import Stack
from models.components.display import Display
from models.components.keyboard import Keyboard
from models.components.timers import Timers
from constants import PROGRAM_START

class Chip8:
    FONT_START = 0x000
    FONTSET = [
        0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
        0x20, 0x60, 0x20, 0x20, 0x70, # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
        0x90, 0x90, 0xF0, 0x10, 0x10, # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
        0xF0, 0x10, 0x20, 0x40, 0x40, # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90, # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
        0xF0, 0x80, 0x80, 0x80, 0xF0, # C
        0xE0, 0x90, 0x90, 0x90, 0xE0, # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
        0xF0, 0x80, 0xF0, 0x80, 0x80, # F
    ]
    
    def __init__(self) -> None:
        self.memory: Memory = Memory()
        self.stack: Stack = Stack()
        self.display: Display = Display()
        self.keyboard: Keyboard = Keyboard()
        self.timers: Timers = Timers()
        
        self.running = True
        
        self.cpu: CPU = CPU(
            self.memory,
            self.stack,
            self.display,
            self.keyboard,
            self.timers
        )
        
        self.load_font()
    
    @property
    def waiting_key(self) -> bool:
        return self.cpu.waiting_key
    
    def reset(self) -> None:
        self.cpu.reset()
    
    def load_font(self) -> None:
        self.memory.load(self.FONT_START, self.FONTSET)

    def load_rom(self, rom: list[int]) -> None:
        self.memory.load(PROGRAM_START, rom)

    def cycle(self) -> None:
        self.cpu.cycle()

    def run(self, cycles=None) -> None:
        if cycles != None and cycles >= 0:
            for _ in range(cycles):
                self.cycle()
            return
        
        while True:
            self.cycle()