class Timers:

    def __init__(self):
        self.delay = 0
        self.sound = 0

    def tick(self):

        if self.delay > 0:
            self.delay -= 1

        if self.sound > 0:
            self.sound -= 1