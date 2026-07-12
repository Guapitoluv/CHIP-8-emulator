from models.chip8 import Chip8

chip8: Chip8 = Chip8()

"""
rom = None

with open(filepath, "rb") as file:
    rom = file.read()

if rom:
    chip8.load_rom(rom)
"""

chip8.load_rom([
    0x60, 0x0A, # 6XNN ADD VX:V0, NN:0A:10
    0x61, 0x0A, # 6XNN ADD VX:V1, NN:0A:10
    0x50, 0x10, # 5XY0 SE VX:V0, VY:V1
    0x61, 0x32, # 6XNN ADD VX:V1, NN:32:50
    0x12, 0x08, # 1NNN JP NNN:208
])

for _ in range(4):
    chip8.cycle()

for i in range(16):
    print(f"V{i}: {chip8.cpu.registers.V[i]}")