from pathlib import Path
from time import sleep

from models.chip8 import Chip8
from models.debugger import Debugger

def show():

    lines = []

    for y in range(chip8.display.HEIGHT):
        line = ""

        for x in range(chip8.display.WIDTH):
            pixel = chip8.display.pixels[y * chip8.display.WIDTH + x]

            line += "██" if pixel else "  "

        lines.append(line)

    with open(Path(__file__).parent / "results.txt", "w") as file:
        file.write("\n".join(lines))

def showVs(c):
    for i in range(16):
        print(f"V{i}: {c.cpu.registers.V[i]}")

def open_ch8rom_file(filepath) -> str | None:
    with open(filepath, "rb") as file:
        return file.read() or None



chip8: Chip8 = Chip8()
debugger: Debugger = Debugger(chip8)

filepath: Path = Path(__file__).parent / "roms/rom002.ch8"

rom: str = open_ch8rom_file(filepath)

rom2 = [hex(i) for i in list(rom)]
rom = [
    0x60, 0x00, # V0 = 0 (caractere 0)
    0xF0, 0x29, # I = sprite do caractere V0
    0x61, 0x05, # V1 = X = 5
    0x62, 0x05, # V2 = Y = 5
    0xD1, 0x25, # Desenha 0
    0x60, 0x01, # V0 = 1 (caractere 1)
    0xF0, 0x29, # I = sprite do caractere V0
    0x61, 0x0F, # V1 = X = 15
    0x62, 0x05, # V2 = Y = 5
    0xD1, 0x25 # Desenha 1
]

if rom:
    def f():
        rom_size = len(rom)
        print("ROM' size:", rom_size)
        if rom_size%2!=0: return
        
        chip8.load_rom(rom)
        
        for i in range(int(rom_size/2)):
            print(f"({i})", end=" ")
            debugger.show_state()
            print()
            chip8.cycle()
            sleep(0.02)
        show()
    f()