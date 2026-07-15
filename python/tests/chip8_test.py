from models.chip8 import Chip8

chip8 = Chip8()

def show():
    line = ""
    j = 0
    for i in range(chip8.display.HEIGHT*chip8.display.WIDTH):
        j += 1
        line += str(chip8.display.pixels[i])
        
        if (j == chip8.display.WIDTH):
            print(line)
            line = ""
            j = 0

def test_DXYN():
    chip8.cpu.registers.I = 0x300
    
    chip8.memory[0x300] = 0b11110000
    
    chip8.cpu.registers.V[0] = 0
    chip8.cpu.registers.V[1] = 0
    
    chip8.cpu.op_DXYN(0xD011)
    
    assert chip8.display.pixels[0] == 1
    assert chip8.display.pixels[1] == 1
    assert chip8.display.pixels[2] == 1
    assert chip8.display.pixels[3] == 1
    
    assert chip8.cpu.registers.V[0xF] == 0
    
    # Desenha novamente (XOR)
    
    chip8.cpu.op_DXYN(0xD011)
    
    assert chip8.display.pixels[0] == 0
    assert chip8.display.pixels[1] == 0
    assert chip8.display.pixels[2] == 0
    assert chip8.display.pixels[3] == 0
    
    assert chip8.cpu.registers.V[0xF] == 1

def test_all():
    ...

test_DXYN()