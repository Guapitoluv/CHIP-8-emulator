from models.components.memory import Memory
from models.components.stack import Stack
from models.components.display import Display
from models.components.keyboard import Keyboard
from models.components.timers import Timers
from models.components.registers import Registers
from models.uintxarray import UInt8Array


class CPU:
    def __init__(
            self,
            memory: Memory,
            stack: Stack,
            display: Display,
            keyboard: Keyboard,
            timers: Timers
    ) -> None:
        self.memory: Memory = memory
        self.stack: Stack = stack
        self.display: Display = display
        self.keyboard: Keyboard = keyboard
        self.timers: Timers = timers

        self.registers: Registers = Registers()

    def fetch(self) -> int:
        opcode: int = (
            (int(self.memory[self.registers.pc]) << 8)
            | int(self.memory[self.registers.pc + 1])
        )

        self.registers.pc += 2
        return opcode

    def cycle(self) -> int:
        opcode: int = self.fetch()
        self.execute(opcode)

    def execute(self, opcode: int):
        match opcode & 0xF000:
            case 0x0000:
                match opcode:
                    case 0x00E0: self.op_00E0()
                    case 0x00EE: self.op_00EE()
            
            case 0x1000: self.op_1NNN(opcode)
            case 0x2000: self.op_2NNN(opcode)
            case 0x3000: self.op_3XNN(opcode)
            case 0x4000: self.op_4XNN(opcode)
            case 0x5000: self.op_5XY0(opcode)
            case 0x6000: self.op_6XNN(opcode)
            case 0x7000: self.op_7XNN(opcode)
            
            case 0x8000: ...
            case 0x9000: ...
            case 0xA000: ...
            case 0xB000: ...
            case 0xC000: ...
            case 0xD000: ...
            case 0xE000: ...
            case 0xF000: ...
            
            case _: raise NotImplementedError(hex(opcode))
    
    def op_00E0(self) -> None:
        self.display.clear()
    
    def op_00EE(self) -> None:
        self.registers.pc = stack.pop()
    
    def op_1NNN(self, opcode: int) -> None:
        self.registers.pc = opcode & 0x0FFF
        
    def op_2NNN(self, opcode: int) -> None:
        self.stack[self.registers.sp] = self.registers.pc
        self.registers.sp += 1
        self.registers.pc = opcode & 0x0FFF
    
    def op_3XNN(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        nn: int = opcode & 0xFF
        
        if (self.registers.V[x] == nn):
            self.registers.pc += 2
    
    def op_4XNN(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        nn: int = opcode & 0xFF
        
        if (self.registers.V[x] != nn):
            self.registers.pc += 2
    
    def op_5XY0(self, opcode):
        x = (opcode >> 8) & 0xF
        y = (opcode >> 4) & 0xF
    
        if self.registers.V[x] == self.registers.V[y]:
            self.registers.pc += 2
    
    def op_6XNN(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        nn: int = opcode & 0xFF

        self.registers.V[x] = nn

    def op_7XNN(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        nn: int = opcode & 0xFF

        self.registers.V[x] = (self.registers.V[x] + nn) & 0xFF
    
    def op_8XY0(self, opcode: int) -> None: ...
    def op_8XY1(self, opcode: int) -> None: ...
    def op_8XY2(self, opcode: int) -> None: ...
    def op_8XY3(self, opcode: int) -> None: ...
    def op_8XY4(self, opcode: int) -> None: ...
    def op_8XY5(self, opcode: int) -> None: ...
    def op_8XY6(self, opcode: int) -> None: ...
    def op_8XY7(self, opcode: int) -> None: ...
    def op_8XY8(self, opcode: int) -> None: ...
    def op_8XY9(self, opcode: int) -> None: ...
    def op_8XYA(self, opcode: int) -> None: ...
    def op_8XYB(self, opcode: int) -> None: ...
    def op_8XYC(self, opcode: int) -> None: ...
    def op_8XYD(self, opcode: int) -> None: ...
    def op_8XYE(self, opcode: int) -> None: ...
    
    def op_9XY0(self, opcode: int) -> None: ...
    def op_ANNN(self, opcode: int) -> None: ...
    def op_BNNN(self, opcode: int) -> None: ...
    def op_CXNN(self, opcode: int) -> None: ...
    
    def op_DXYN(self, opcode):
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        height: int = opcode & 0xF
        
        pos_x: int = self.registers.V[x]
        pos_y: int = self.registers.V[y]
        
        collision = self.display.draw_sprite(
            pos_x,
            pos_y,
            self.memory,
            self.I,
            height
        )
    
        self.V[0xF] = 1 if collision else 0
    
    def op_EX9E(self, opcode: int) -> None: ...
    def op_EXA1(self, opcode: int) -> None: ...
    
    def op_FX07(self, opcode: int) -> None:
        ...
    def op_FX65(self, opcode: int) -> None: ...
    