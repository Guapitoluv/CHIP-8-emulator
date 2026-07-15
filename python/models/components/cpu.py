from random import getrandbits

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
        
        self.waiting_key = False

        self.registers: Registers = Registers()
    
    
    def reset(self) -> None:
        self.op_00E0()
        self.registers.reset()
        self.keyboard.reset()
    
    
    @staticmethod
    def make_opcode(high_byte: int, low_byte: int) -> int:
        return (high_byte << 8) | low_byte
    
    
    def fetch(self) -> int:
        high_byte = int(self.memory[self.registers.pc])
        low_byte = int(self.memory[self.registers.pc + 1])
        
        opcode = self.make_opcode(high_byte, low_byte)
        
        self.registers.pc += 2
        return opcode
    
    
    def cycle(self) -> None:
        opcode: int = self.fetch()
        self.execute(opcode)
    
    
    def execute(self, opcode: int) -> None:
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
            
            case 0x8000:
                match opcode & 0xF:
                    case 0x0: self.op_8XY0(opcode)
                    case 0x1: self.op_8XY1(opcode)
                    case 0x2: self.op_8XY2(opcode)
                    case 0x3: self.op_8XY3(opcode)
                    case 0x4: self.op_8XY4(opcode)
                    case 0x5: self.op_8XY5(opcode)
                    case 0x6: self.op_8XY6(opcode)
                    case 0x7: self.op_8XY7(opcode)
                    case 0xE: self.op_8XYE(opcode)
            
            case 0x9000: self.op_9XY0(opcode) # SNE Vx, Vy
            case 0xA000: self.op_ANNN(opcode) # LD I, addr
            case 0xB000: self.op_BNNN(opcode) # JP V0, addr
            case 0xC000: self.op_CXNN(opcode) # RND Vx, byte
            case 0xD000: self.op_DXYN(opcode) # DRW Vx, Vy, nibble
            
            case 0xE000:
                match opcode & 0xFF:
                    case 0x9E: self.op_EX9E(opcode) # SKP Vx
                    case 0xA1: self.op_EXA1(opcode) # SKNP Vx
            
            case 0xF000:
                match opcode & 0xFF:
                    case 0x07: self.op_FX07(opcode)
                    case 0x0A: self.op_FX0A(opcode)
                    case 0x15: self.op_FX15(opcode)
                    case 0x18: self.op_FX18(opcode)
                    case 0x1E: self.op_FX1E(opcode)
                    case 0x29: self.op_FX29(opcode)
                    case 0x33: self.op_FX33(opcode)
                    case 0x55: self.op_FX55(opcode)
                    case 0x65: self.op_FX65(opcode)
            
            case _: raise NotImplementedError(hex(opcode))
    
    # ================================================
    #     0'S CASES
    # ================================================
    
    def op_00E0(self) -> None:
        self.display.clear()
    
    def op_00EE(self) -> None:
        self.registers.pc = stack.pop()
    
    # ================================================
    #     CASE 1 -> CASE 7
    # ================================================
    
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
    
    # ================================================
    #     8XY_'s CASES I
    # ================================================
    
    def op_8XY0(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[x] = self.registers.V[y]
    
    def op_8XY1(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[x] |= self.registers.V[y]
    
    def op_8XY2(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[x] &= self.registers.V[y]
    
    def op_8XY3(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[x] ^= self.registers.V[y]
    
    def op_8XY4(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        result = (
            int(self.registers.V[x])
            + int(self.registers.V[y])
        )
        
        self.registers.V[0xF] = int(result > 0xFF)
        self.registers.V[x] = result & 0xFF
    
    def op_8XY5(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[0xF] = int(
            self.registers.V[x]
            >= self.registers.V[y]
        )
        
        self.registers.V[x] = (
            self.registers.V[x]
            - self.registers.V[y]
        ) & 0xFF
    
    def op_8XY6(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[0xF] = int(
            self.registers.V[y] & 0x01
        )
        
        self.registers.V[x] = self.registers.V[y] >> 1
    
    def op_8XY7(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[0xF] = int(
            self.registers.V[y]
            >= self.registers.V[x]
        )
        
        self.registers.V[x] = (
            self.registers.V[y]
            - self.registers.V[x]
        ) & 0xFF
    
    def op_8XYE(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        self.registers.V[0xF] = (
            self.registers.V[x] >> 7
        ) & 1
    
        self.registers.V[x] = (
            self.registers.V[x] << 1
        ) & 0xFF
    
    # ================================================
    #     CASE 9 -> CASE D
    # ================================================
    
    def op_9XY0(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        y: int = (opcode >> 4) & 0xF
        
        if self.registers.V[x] != self.registers.V[y]:
            self.registers.pc += 2
    
    def op_ANNN(self, opcode: int) -> None:
        self.registers.I = opcode & 0x0FFF
    
    def op_BNNN(self, opcode: int) -> None:
        self.registers.pc = (
            (opcode & 0xFFF)
            + int(self.registers.V[0])
        )
    
    def op_CXNN(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        nn: int = opcode & 0xFF
    
        rnd = getrandbits(8)
    
        self.registers.V[x] = rnd & nn
    
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
            self.registers.I,
            height
        )
    
        self.registers.V[0xF] = 1 if collision else 0
    
    # ================================================
    #     E's CASES
    # ================================================
    
    def op_EX9E(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        if self.keyboard.is_pressed(self.registers.V[x]):
            self.registers.pc += 2
    
    def op_EXA1(self, opcode: int) -> None:
        x: int = (opcode >> 8) & 0xF
        if not self.keyboard.is_pressed(self.registers.V[x]):
            self.registers.pc += 2
    
    # ================================================
    #     FX__'s CASES
    # ================================================
    
    def op_FX07(self, opcode: int) -> None:
        # LD VX, DT
        # VX recebe o valor do delay timer
        x: int = (opcode >> 8) & 0xF
    
        self.registers.V[x] = self.timers.delay_timer
    
        
    def op_FX0A(self, opcode: int) -> None:
        # LD VX, K
        x = (opcode >> 8) & 0xF
        key = self.keyboard.get_key()
        
        
        if key is None:
            self.waiting_key = True
            self.registers.pc -= 2
            return
        
        self.waiting_key = False
        self.registers.V[x] = key
    
    
    def op_FX15(self, opcode: int) -> None:
        # LD DT, VX
        # Delay timer recebe VX
    
        x: int = (opcode >> 8) & 0xF
    
        self.timers.delay_timer = self.registers.V[x]
    
    
    def op_FX18(self, opcode: int) -> None:
        # LD ST, VX
        # Sound timer recebe VX
    
        x: int = (opcode >> 8) & 0xF
    
        self.timers.sound_timer = self.registers.V[x]
    
    
    def op_FX1E(self, opcode: int) -> None:
        # ADD I, VX
        # I += VX
    
        x: int = (opcode >> 8) & 0xF
    
        self.registers.I += self.registers.V[x]
    
    def op_FX29(self, opcode: int) -> None:
        # LD F, VX
        # I aponta para o sprite hexadecimal do caractere em VX
    
        x: int = (opcode >> 8) & 0xF
        digit = self.registers.V[x]
        self.registers.I = digit * 5
    
    
    def op_FX33(self, opcode: int) -> None:
        # LD B, VX
        # Guarda a representação decimal de VX na memória
    
        x: int = (opcode >> 8) & 0xF
    
        value = int(self.registers.V[x])
    
        hundreds = value // 100
        tens = (value // 10) % 10
        units = value % 10
    
        self.memory[self.registers.I] = hundreds
        self.memory[self.registers.I + 1] = tens
        self.memory[self.registers.I + 2] = units
    
    
    def op_FX55(self, opcode: int) -> None:
        # LD [I], VX
        # Copia V0 até VX para memória começando em I
    
        x: int = (opcode >> 8) & 0xF
    
        for i in range(x + 1):
            self.memory[self.registers.I + i] = self.registers.V[i]
    
    
    def op_FX65(self, opcode: int) -> None:
        # LD VX, [I]
        # Carrega memória para V0 até VX
    
        x: int = (opcode >> 8) & 0xF
    
        for i in range(x + 1):
            self.registers.V[i] = iself.memory[self.registers.I + i]