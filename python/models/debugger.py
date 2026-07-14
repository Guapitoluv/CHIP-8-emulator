from models.disassembler import Disassembler as disblr

class Debugger:
    def __init__(self, chip8):
        self.chip8 = chip8
    
    def peek_opcode(self) -> int:
        cpu = self.chip8.cpu
        regs = cpu.registers
        
        high_byte = int(cpu.memory[regs.pc])
        low_byte = int(cpu.memory[regs.pc + 1])
        
        return cpu.make_opcode(high_byte, low_byte)
    
    
    def show_state(self):
        cpu = self.chip8.cpu
        regs = cpu.registers
        op = self.peek_opcode()

        print("=== CHIP-8 STATE ===")

        print(f"PC: {hex(regs.pc)}")
        print(f"I : {hex(regs.I)}")
        print(f"SP: {regs.sp}")
        
        print(f"opcode: {hex(op)}")
        print(f"instruction: {disblr.disassemble(op)}")

        print("\nRegisters:")
        for i, value in enumerate(regs.V):
            print(f"V{i:X}: {int(value):02X}")

        print("\nStack:")
        for i in range(regs.sp):
            print(f"[{i}] {hex(int(cpu.stack[i]))}")

        print("\nTimers:")
        print(f"DT: {cpu.timers.dt}")
        print(f"ST: {cpu.timers.st}")

        print("\nDisplay:")
        print(f"{cpu.display.WIDTH}x{cpu.display.HEIGHT}")