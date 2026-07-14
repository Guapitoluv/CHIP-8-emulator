from models.uintxarray import UInt8Array


class Registers:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        # Registradores de propósito geral (V0-VF)
        self.V = UInt8Array(16)

        # Registrador de índice
        self.I = 0

        # Program Counter
        self.pc = 0x200

        # Stack Pointer
        self.sp = 0

        # Timers
        self.delay = 0
        self.sound = 0