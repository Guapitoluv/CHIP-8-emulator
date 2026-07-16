import re


class Chip8Assembler:
    def __init__(self) -> None:
        self.labels = {}

        self.instructions = [
            (r"^SYS\s+(\S+)$", self.sys),
            (r"^CLS$", self.cls),
            (r"^RET$", self.ret),

            (r"^JP\s+(\S+)$", self.jp),
            (r"^CALL\s+(\S+)$", self.call),
            (r"^SE\s+V([0-9A-F]),\s*([0-9A-F]+)$", self.se_byte),
            (r"^SNE\s+V([0-9A-F]),\s*([0-9A-F]+)$", self.sne_byte),

            (r"^SE\s+V([0-9A-F]),\s*V([0-9A-F])$", self.se_reg),
            (r"^LD\s+V([0-9A-F]),\s*([0-9A-F]+)$", self.ld_byte),
            (r"^ADD\s+V([0-9A-F]),\s*([0-9A-F]+)$", self.add_byte),

            (r"^LD\s+V([0-9A-F]),\s*V([0-9A-F])$", self.ld_reg),
            (r"^OR\s+V([0-9A-F]),\s*V([0-9A-F])$", self.or_reg),
            (r"^AND\s+V([0-9A-F]),\s*V([0-9A-F])$", self.and_reg),
            (r"^XOR\s+V([0-9A-F]),\s*V([0-9A-F])$", self.xor_reg),
            (r"^ADD\s+V([0-9A-F]),\s*V([0-9A-F])$", self.add_reg),
            (r"^SUB\s+V([0-9A-F]),\s*V([0-9A-F])$", self.sub_reg),
            (r"^SHR\s+V([0-9A-F])$", self.shr),
            (r"^SUBN\s+V([0-9A-F]),\s*V([0-9A-F])$", self.subn),
            (r"^SHL\s+V([0-9A-F])$", self.shl),

            (r"^SNE\s+V([0-9A-F]),\s*V([0-9A-F])$", self.sne_reg),

            (r"^LD\s+I,\s*(\S+)$", self.ld_i),
            (r"^JP\s+V0,\s*(\S+)$", self.jp_v0),

            (r"^RND\s+V([0-9A-F]),\s*([0-9A-F]+)$", self.rnd),
            (r"^DRW\s+V([0-9A-F]),\s*V([0-9A-F]),\s*([0-9A-F])$", self.drw),

            (r"^SKP\s+V([0-9A-F])$", self.skp),
            (r"^SKNP\s+V([0-9A-F])$", self.sknp),

            (r"^LD\s+V([0-9A-F]),\s*DT$", self.ld_v_dt),
            (r"^LD\s+V([0-9A-F]),\s*K$", self.ld_v_key),
            (r"^LD\s+DT,\s*V([0-9A-F])$", self.ld_dt_v),
            (r"^LD\s+ST,\s*V([0-9A-F])$", self.ld_st_v),

            (r"^ADD\s+I,\s*V([0-9A-F])$", self.add_i_v),
            (r"^LD\s+F,\s*V([0-9A-F])$", self.ld_f),
            (r"^LD\s+B,\s*V([0-9A-F])$", self.ld_b),
            (r"^LD\s+\[I\],\s*V([0-9A-F])$", self.ld_mem),
            (r"^LD\s+V([0-9A-F]),\s*\[I\]$", self.ld_reg_mem),
        ]
    
    
    def assemble_instruction(self, line) -> int:
        line = line.upper().strip()

        for pattern, func in self.instructions:
            m = re.fullmatch(pattern, line)
            if m: return func(*m.groups())

        raise Exception(f"Unknown instruction: {line}")
    
    
    def r(self, x) -> int:
        """Resolve um token numérico: tenta hex primeiro, depois procura na
        tabela de labels. Isso é usado tanto pros registradores (V0-VF)
        quanto pros endereços/valores imediatos."""
        try: return int(x, 16)
        except ValueError:
            if x in self.labels: return self.labels[x]
            raise Exception(f"Undefined label: {x}")
    
    
    # 0x0---
    def sys(self,a) -> int: return self.r(a)
    def cls(self) -> int:   return 0x00E0
    def ret(self) -> int:   return 0x00EE

    # 1---
    def jp(self,a) -> int: return 0x1000 | self.r(a)

    # 2---
    def call(self,a) -> int: return 0x2000 | self.r(a)

    def se_byte(self,x,k) -> int:  return 0x3000 | self.r(x)<<8 | self.r(k)
    def sne_byte(self,x,k) -> int: return 0x4000 | self.r(x)<<8 | self.r(k)
    def se_reg(self,x,y) -> int:   return 0x5000 | self.r(x)<<8 | self.r(y)<<4
    
    def ld_byte(self,x,k) -> int:  return 0x6000 | self.r(x)<<8 | self.r(k)
    def add_byte(self,x,k) -> int: return 0x7000 | self.r(x)<<8 | self.r(k)
    
    def ld_reg(self,x,y) -> int:  return 0x8000 | self.r(x)<<8 | self.r(y)<<4
    def or_reg(self,x,y) -> int:  return 0x8001 | self.r(x)<<8 | self.r(y)<<4
    def and_reg(self,x,y) -> int: return 0x8002 | self.r(x)<<8 | self.r(y)<<4
    def xor_reg(self,x,y) -> int: return 0x8003 | self.r(x)<<8 | self.r(y)<<4
    def add_reg(self,x,y) -> int: return 0x8004 | self.r(x)<<8 | self.r(y)<<4
    def sub_reg(self,x,y) -> int: return 0x8005 | self.r(x)<<8 | self.r(y)<<4
    def shr(self,x) -> int:       return 0x8006 | self.r(x)<<8
    def subn(self,x,y) -> int:    return 0x8007 | self.r(x)<<8 | self.r(y)<<4
    def shl(self,x) -> int:       return 0x800E | self.r(x)<<8
    
    def sne_reg(self,x,y) -> int: return 0x9000 | self.r(x)<<8 | self.r(y)<<4
    
    def ld_i(self,a) -> int:  return 0xA000 | self.r(a)
    def jp_v0(self,a) -> int: return 0xB000 | self.r(a)
    
    def rnd(self,x,k) -> int:   return 0xC000 | self.r(x)<<8 | self.r(k)
    def drw(self,x,y,n) -> int: return 0xD000 | self.r(x)<<8 | self.r(y)<<4 | self.r(n)
    
    def skp(self,x) -> int:  return 0xE09E | self.r(x)<<8
    def sknp(self,x) -> int: return 0xE0A1 | self.r(x)<<8
    
    def ld_v_dt(self,x) -> int:  return 0xF007 | self.r(x)<<8
    def ld_v_key(self,x) -> int: return 0xF00A | self.r(x)<<8
    def ld_dt_v(self,x) -> int:  return 0xF015 | self.r(x)<<8
    def ld_st_v(self,x) -> int:  return 0xF018 | self.r(x)<<8
    
    def add_i_v(self,x) -> int:    return 0xF01E | self.r(x)<<8
    def ld_f(self,x) -> int:       return 0xF029 | self.r(x)<<8
    def ld_b(self,x) -> int:       return 0xF033 | self.r(x)<<8
    def ld_mem(self,x) -> int:     return 0xF055 | self.r(x)<<8
    def ld_reg_mem(self,x) -> int: return 0xF065 | self.r(x)<<8


    def assemble(self, source) -> bytes:
        # Instruções podem ser separadas por ';' ou por quebra de linha.
        raw_chunks = re.split(r"[;\n]", source)
        chunks = [c.strip() for c in raw_chunks if c.strip()]

        label_def = re.compile(r"^(\w+):\s*(.*)$")

        # --- Passagem 1: descobrir o endereço de cada label ---------------
        # Cada instrução ocupa 2 bytes, e o programa começa em 0x200
        # (é onde o interpretador CHIP-8 carrega a ROM na RAM).
        self.labels = {}
        pending = []  # instruções "puras", já sem a parte de label
        address = 0x200

        for chunk in chunks:
            upline = chunk.upper()
            m = label_def.match(upline)

            if m:
                name, rest = m.group(1), m.group(2).strip()
                if name in self.labels:
                    raise Exception(f"Label redefinida: {name}")
                self.labels[name] = address

                if rest:
                    pending.append(rest)
                    address += 2
            else:
                pending.append(upline)
                address += 2

        # --- Passagem 2: montar de fato, agora com as labels resolvidas ---
        result = []
        for instr in pending:
            opcode = self.assemble_instruction(instr)
            result.append(opcode >> 8)
            result.append(opcode & 0xFF)

        return bytes(result)