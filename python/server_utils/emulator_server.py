import asyncio
import json
import time

from models.message import WaitingKeyMsg, DisplayMsg, SoundMsg


class EmulatorServer:
    def __init__(self, chip8) -> None:
        self.chip8 = chip8
        self.last_timer = time.monotonic()
        self.last_display = time.monotonic()
        self.sent_waiting = False
        self.sent_sound = False
    
    
    async def emulator_loop(self, ws):
        while self.chip8.running:
            self.run_cpu()
            await self.update_waiting_key(ws)
            await self.update_timers(ws)
            await self.update_display(ws)
            await asyncio.sleep(0.001)
    
    
    def run_cpu(self):
        for _ in range(25):
            self.chip8.cycle()
            
            if self.chip8.waiting_key:
                break
    
    
    async def update_waiting_key(self, ws):
        if self.chip8.waiting_key and not self.sent_waiting:
            print("sending waiting key")
            await WaitingKeyMsg().send(ws)
            print("sent waiting key")
            self.sent_waiting = True
        
        if not self.chip8.waiting_key:
            self.sent_waiting = False
    
    
    async def update_timers(self, ws):
        now = time.monotonic()
        
        # Atualiza timers em 60Hz
        while now - self.last_timer >= 1/60:
            self.chip8.timers.tick()
            self.last_timer += 1/60
            
            sound_running = self.chip8.timers.st > 0
            
            if sound_running != self.sent_sound:
                print("sending_sound")
                await SoundMsg(sound_running).send(ws)
                self.sent_sound = sound_running
    
    
    async def update_display(self, ws):
        now = time.monotonic()
        
        if now - self.last_display >= 1/60:
            await DisplayMsg(self.chip8.display.pixels.tolist()).send(ws)
            self.last_display += 1/60