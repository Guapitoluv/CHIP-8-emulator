from models.uintxarray import UInt8Array, UInt16Array 

# CHIP-8

# ===================================
# CPU STRUCTURE
# ===================================
memory: UInt8Array = UInt8Array(4096)
stack: UInt16Array = UInt16Array(16)
V: UInt8Array = UInt8Array(16) # Registers
pc: int = 0x200 # Program Counter
sp: int = 0 # Stack Pointer
I: int = 0 # Index Register


memory[0x200] = 0x60; memory[0x201] = 0x0A; # LD V0, 0x0A   (V0 = 10)
memory[0x202] = 0x70; memory[0x203] = 0x05; # ADD V0, 0x05  (V0 += 5)
memory[0x204] = 0x61; memory[0x205] = 0x32; # LD V1, 0x32   (V1 = 50)
memory[0x206] = 0x12; memory[0x207] = 0x08; # JP 0x208      (pula pra linha seguinte = "fim")

# ===================================
# FETCH-DECODE-EXECUTE
# ===================================
executing: bool = True
counter: int = 0
SAFETY_LIMIT: int = 20

high_byte: int
low_byte: int
opcode: int
x: int
nn: int
nnn: int

while (executing and counter < SAFETY_LIMIT):
    counter += 1
    
    # ---- FETCH ----
    high_byte = int(memory[pc])
    low_byte = int(memory[pc+1])
    opcode = (high_byte << 8) | low_byte
    
    # ---- DECODE ----
    mytype = (opcode & 0xF000) >> 12
    x = (opcode & 0xF00) >> 8
    nn = opcode & 0x00FF
    nnn = opcode & 0x0FFF
    
    # ---- EXECUTE ----
    match (mytype):
        case 0x6: # 6XNN: LD VX, NN
            V[x] = nn
            pc += 2
    
        case 0x7: # 7XNN: ADD VX, NN
            V[x] = (V[x] + nn) & 0xFF # & 0xFF garante o "estouro" de 8 bits, como vimos antes
            pc += 2
    
        case 0x1: # 1NNN: JP NNN
            if (nnn == pc):
                # Detectamos que o programa pulou pra ELE MESMO = loop infinito
                # intencional (assim como ROMs reais de CHIP-8 terminam).
                executing = False
            pc = nnn
    
        case _:
          executing = False

# showing:
for i in range(len(V)): print(f"V{i}: {V[i]}")