class Timers:
    def __init__(self):
        self.dt = 0
        self.st = 0

    def tick(self):
        if self.dt > 0:
            self.dt -= 1
        
        if self.st > 0:
            self.st -= 1