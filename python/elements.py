from pathlib import Path

from models.chip8 import Chip8
from models.debugger import Debugger
from models.assembler import Chip8Assembler
from server_utils.emulator_server import EmulatorServer

chip8: Chip8 = Chip8()
debugger: Debugger = Debugger(chip8)
emulator_server = EmulatorServer(chip8, debugger)
filepath = Path(__file__).parent / "roms"

with open(filepath / "to_assemble/pong_source.asm", "r") as file:
    rom = Chip8Assembler().assemble(file.read())

with open(filepath / "ch8/pong.ch8", "wb") as file:
    file.write(rom)

with open(filepath / "ch8/pong.ch8", "rb") as file:
    rom = file.read()

clients: set = set()