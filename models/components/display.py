from models.uintxarray import UInt8Array


class Display:

    WIDTH = 64
    HEIGHT = 32

    def __init__(self):
        self.pixels = UInt8Array(self.WIDTH * self.HEIGHT)

    def clear(self):
        self.pixels.fill(0)
    
    def draw_sprite(self, x, y, memory, address, height):
        collision = False
        
        for row in range(height):
            sprite_byte = int(memory[address + row])
            
            for col in range(8):
                sprite_pixel = sprite_byte & (0x80 >> col)
                
                if sprite_pixel:
                    px = (x + col) % self.WIDTH
                    py = (y + row) % self.HEIGHT
                    
                    index = py * self.WIDTH + px
                    
                    # Detecta colisão antes do XOR
                    if self.pixels[index] == 1:
                        collision = True
                    
                    # XOR: liga ou desliga o pixel
                    self.pixels[index] ^= 1
        
        return collision