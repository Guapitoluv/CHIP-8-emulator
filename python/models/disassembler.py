class Disassembler:
    @staticmethod
    def disassemble(opcode: int) -> str:
        match opcode & 0xF000:

            case 0x0000:
                match opcode:
                    case 0x00E0: return "CLS"
                    case 0x00EE: return "RET"

            case 0x1000: return f"JP {hex(opcode & 0x0FFF)}"
            case 0x2000: return f"CALL {hex(opcode & 0x0FFF)}"
            case 0x3000: return f"SE V{(opcode >> 8) & 0xF:X}, {hex(opcode & 0xFF)}"
            case 0x6000: return f"LD V{(opcode >> 8) & 0xF:X}, {hex(opcode & 0xFF)}"
            case 0x7000: return f"ADD V{(opcode >> 8) & 0xF:X}, {hex(opcode & 0xFF)}"
            case 0xA000: return f"LD I, {hex(opcode & 0xFFF)}"
            case 0xD000: return f"DRW V{(opcode >> 8) & 0xF:X}, V{(opcode >> 4) & 0xF:X}, {opcode & 0xF}"
            
            case 0xF000:
                match opcode & 0xFF:
                    case 0x07: return f"LD V{(opcode >> 8) & 0xF}, DT"
                    case 0x0A: return f"LD V{(opcode >> 8) & 0xF}, K"
                    case 0x15: return f"LD DT, V{(opcode >> 8) & 0xF}"
                    case 0x18: return f"LD ST, V{(opcode >> 8) & 0xF}"
                    case 0x1E: return f"ADD I, V{(opcode >> 8) & 0xF}"
                    case 0x29: return f"LD F, V{(opcode >> 8) & 0xF}"
                    case 0x33: return f"LD B, V{(opcode >> 8) & 0xF}"
                    case 0x55: return f"LD [I], V0-V{(opcode >> 8) & 0xF}"
                    case 0x65: return f"LD V0-V{(opcode >> 8) & 0xF}, [I]"
            
            case _:
                return f"UNKNOWN {hex(opcode)}"