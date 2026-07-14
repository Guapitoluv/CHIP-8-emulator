from models.uintxarray import UInt8Array
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

class Display:

    WIDTH = DISPLAY_WIDTH
    HEIGHT = DISPLAY_HEIGHT

    def __init__(self):
        self.pixels = UInt8Array(self.WIDTH * self.HEIGHT)

    def clear(self):
        self.pixels.fill(0)
    
    def draw_sprite(self, x, y, memory, address, height):
        collision = False
    
        x = int(x)
        y = int(y)
    
        for row in range(height):
            sprite_byte = int(memory[address + row])
    
            for col in range(8):
                if sprite_byte & (0x80 >> col):
    
                    px = (x + col) % self.WIDTH
                    py = (y + row) % self.HEIGHT
    
                    index = int(py) * int(self.WIDTH) + int(px)
    
                    if self.pixels[index] == 1:
                        collision = True
    
                    self.pixels[index] ^= 1

        return collision