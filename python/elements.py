from models.chip8 import Chip8
from models.debugger import Debugger
from server_utils.emulator_server import EmulatorServer

chip8: Chip8 = Chip8()
debugger: Debugger = Debugger(chip8)
emulator_server = EmulatorServer(chip8)
clients: set = set()