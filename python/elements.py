from models.chip8 import Chip8
from models.debugger import Debugger

chip8 = Chip8()
debugger = Debugger(chip8) 
clients = set()