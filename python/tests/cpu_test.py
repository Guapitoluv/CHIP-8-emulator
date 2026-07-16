from models.components.memory import Memory
from models.components.stack import Stack
from models.components.display import Display
from models.components.keyboard import Keyboard
from models.components.timers import Timers
from models.components.cpu import CPU

# A: Not using execute cause fetch increment the pc

cpu: CPU = CPU(
    Memory(),
    Stack(),
    Display(),
    Keyboard(),
    Timers()
)


def test_6XNN() -> None:
    cpu.execute(0x600A) # LD VX:V0:00, NN:0A:10
    assert cpu.registers.V[0] == 10


def test_7XNN() -> None:
    cpu.registers.V[0] = 10
    cpu.execute(0x7005) # ADD VX:V0:0A:10, NN:05
    assert cpu.registers.V[0] == 15


def test_add_overflow() -> None:
    # It pops a Warning
    cpu.registers.V[0] = 250
    cpu.execute(0x700A) # ADD VX:V0:FF:250, NN:0A:10
    assert cpu.registers.V[0] == 4 # 260 & 0xFF


def test_1NNN() -> None:
    cpu.registers.pc = 0x300
    cpu.execute(0x1200) # JP NNN:200
    assert cpu.registers.pc == 0x200


def test_2NNN() -> None: #A
    # CALL NNN:200
    cpu.memory[0x200] = 0x22
    cpu.memory[0x201] = 0x00
    
    cpu.cycle()
    
    assert cpu.registers.sp == 1 #deu erro
    assert cpu.stack[0] == 0x202
    assert cpu.registers.pc == 0x200


def test_3XNN() -> None: #A
    cpu.registers.V[0] = 5
    
    # SE VX:V0:5, NN:05
    cpu.memory[0x200] = 0x30
    cpu.memory[0x201] = 0x05
    
    cpu.cycle()
    
    assert cpu.registers.pc == 0x204


def test_no_skip() -> None:
    cpu.registers.V[0] = 4

    # SE VX:V0:5, NN:05
    cpu.memory[0x200] = 0x30
    cpu.memory[0x201] = 0x05
    
    cpu.cycle()

    assert cpu.registers.pc == 0x202


def test_8XY0() -> None:
    cpu.registers.V[0] = 4
    cpu.registers.V[1] = 5
    cpu.execute(0x8010)
    assert cpu.registers.V[0] == cpu.registers.V[1]


def test_8XY1() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x10
    cpu.execute(0x8011) # OR VX:V0:01, VY:V1:10:16
    assert cpu.registers.V[0] == 0x11


def test_8XY2() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x10
    cpu.execute(0x8012) # AND VX:V0:01, VY:V1:10:16
    assert cpu.registers.V[0] == 0x00
    
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x01
    cpu.execute(0x8012) # AND VX:V0:01, VY:V1:01
    assert cpu.registers.V[0] == 0x01


def test_8XY3() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x10
    cpu.execute(0x8013) # XOR VX:V0:01, VY:V1:10:16
    assert cpu.registers.V[0] == 0x11
    
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x01
    cpu.execute(0x8013) # XOR VX:V0:01, VY:V1:01
    assert cpu.registers.V[0] == 0x00


def test_8XY4() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x10
    cpu.execute(0x8014) # ADD VX:V0:01, VY:V1:10:16
    assert cpu.registers.V[0] == 0x11
    assert cpu.registers.V[0xF] == 0


def test_add_overflow_carry() -> None:
    cpu.registers.V[0] = 0xFF
    cpu.registers.V[1] = 0x02
    
    cpu.execute(0x8014) # ADD VX:V0:FF:255, VY:V1:02
    
    assert cpu.registers.V[0] == 0x01
    assert cpu.registers.V[0xF] == 1


def test_8XY5() -> None:
    cpu.registers.V[0] = 0x02
    cpu.registers.V[1] = 0x01
    
    cpu.execute(0x8015) # SUB VX:V0:02, VY:V1:01
    
    assert cpu.registers.V[0] == 0x01
    assert cpu.registers.V[0xF] == 1


def test_8XY5_with_borrow() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x02
    
    cpu.execute(0x8015) # SUB VX:V0:01, VY:V1:02
    
    assert cpu.registers.V[0] == 0xFF
    assert cpu.registers.V[0xF] == 0


def test_8XY6() -> None:
    cpu.registers.V[0] = 0x02 #0010
    cpu.execute(0x8006) # SHR VX:V0:02, VY:V0:02
    assert cpu.registers.V[0] == 0x01
    assert cpu.registers.V[0xF] == 0


def test_8XY6_with_rest() -> None:
    cpu.registers.V[0] = 0x03 #0011
    cpu.execute(0x8006) # SHR VX:V0:03, VY:V0:03
    assert cpu.registers.V[0] == 0x01
    assert cpu.registers.V[0xF] == 1


def test_8XY7() -> None:
    cpu.registers.V[0] = 0x02
    cpu.registers.V[1] = 0x01
    
    cpu.execute(0x8017) # SUBN VX:V0:02, VY:V1:01
    
    assert cpu.registers.V[0] == 0xFF
    assert cpu.registers.V[0xF] == 0


def test_8XY7_with_borrow() -> None:
    cpu.registers.V[0] = 0x01
    cpu.registers.V[1] = 0x02
    
    cpu.execute(0x8017) # SUN VX:V0:01, VY:V1:02
    
    assert cpu.registers.V[0] == 0x01
    assert cpu.registers.V[0xF] == 1


def test_8XYE() -> None:
    cpu.registers.V[0] = 0x02 #0010
    cpu.execute(0x800E) # SHL VX:V0:02, VY:V0:02
    assert cpu.registers.V[0] == 0x04 #0100
    assert cpu.registers.V[0xF] == 0


def test_8XYE_with_rest() -> None:
    cpu.registers.V[0] = 0x08 << 4
    cpu.execute(0x800E) # SHL VX:V0:03, VY:V0:03
    assert cpu.registers.V[0] == 0x00
    assert cpu.registers.V[0xF] == 1


def test_9XY0() -> None:
    cpu.registers.V[0] = 0x02
    cpu.registers.V[1] = 0x01
    cpu.execute(0x9010) # SNE VX:V0:02, VY:V1:01
    assert cpu.registers.pc == 0x202


def test_9XY0_no_skip() -> None:
    cpu.registers.V[0] = 0x02
    cpu.registers.V[1] = 0x02
    cpu.execute(0x9010) # SNE VX:V0:02, VY:V1:02
    assert cpu.registers.pc == 0x200


def test_ANNN() -> None:
    cpu.execute(0xA230) # LD I:230:?
    assert cpu.registers.I == 0x230


def test_BNNN() -> None:
    cpu.execute(0xB230) # LD I:230:?
    assert cpu.registers.pc == 0x230


def test_CXNN() -> None:
    cpu.execute(0xC020) # LD I:230:?
    assert 0 <= cpu.registers.V[0] <= 0x20


def test_EX9E() -> None:
    cpu.registers.V[0] = 0xA
    cpu.keyboard.press(0xA)
    cpu.execute(0xE09E) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x202


def test_EX9E_not_pressed() -> None:
    cpu.registers.V[0] = 0xA
    cpu.execute(0xE09E) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x200
    
    cpu.keyboard.press(0xA)
    cpu.keyboard.release(0xA)
    cpu.execute(0xE09E) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x200


def test_EXA1() -> None:
    cpu.registers.V[0] = 0xA
    cpu.keyboard.press(0xA)
    cpu.execute(0xE0A1) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x200


def test_EXA1_not_pressed() -> None:
    cpu.registers.V[0] = 0xA
    cpu.execute(0xE0A1) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x202
    
    cpu.keyboard.press(0xA)
    cpu.keyboard.release(0xA)
    cpu.execute(0xE0A1) # SKP VX:V0:0A
    assert cpu.registers.pc == 0x204


def test_rom() -> None:
    program = [
        0x60,0x05,  # V0 = 5
        0x70,0x03,  # V0 += 3
        0x61,0x02   # V1 = 2
    ]
    cycles = len(program)/2
    
    if (cycles%2==0):
        raise ValueError("Expecting pairs for each cycles")
    
    chip8.load_rom(program)
    
    for _ in range(cycles):
        chip8.cycle()


def test_all() -> None:
    all_tests = [
        test_6XNN, test_7XNN, test_add_overflow,
        test_1NNN, test_2NNN, test_3XNN,
        test_no_skip, test_8XY0, test_8XY1,
        test_8XY2, test_8XY3, test_8XY4,
        test_add_overflow_carry, test_8XY5,
        test_8XY5_with_borrow, test_8XY6,
        test_8XY6_with_rest, test_8XY7,
        test_8XY7_with_borrow, test_8XYE,
        test_8XYE_with_rest, test_9XY0,
        test_9XY0_no_skip, test_ANNN,
        test_BNNN, test_CXNN, test_EX9E,
        test_EX9E_not_pressed, test_EXA1,
        test_EXA1_not_pressed
    ]
    
    for test in all_tests:
        cpu.reset()
        test()


test_all()        