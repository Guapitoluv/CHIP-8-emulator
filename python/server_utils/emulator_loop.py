import asyncio
import json
import time

from elements import chip8, debugger
from server_utils.send_display import send_display

async def emulator_loop(ws):
    print("emulator")
    last_timer = time.monotonic()
    last_display = time.monotonic()
    
    sent_waiting = False
    sent_sound = False
    
    while chip8.running:
        print("k")
        # Executa CPU
        for _ in range(25):
            chip8.cycle()
            #print(hex(debuggers.peek_opcode()))
            
            if chip8.waiting_key:
                break
        
        # Avisar que está esperando tecla
        if chip8.waiting_key and not sent_waiting:
            print("sending waiting key")
            await ws.send(json.dumps({
                "type": "waiting_key"
            }))
            print("sent waiting key")
            sent_waiting = True
        
        if not chip8.waiting_key:
            sent_waiting = False
        
        now = time.monotonic()
        
        # Atualiza timers em 60Hz
        while now - last_timer >= 1/60:
            chip8.timers.tick()
            last_timer += 1/60
            
            sound_running = chip8.timers.st > 0
            
            if sound_running != sent_sound:
                print("sending_sound")
                await ws.send(json.dumps({
                    "type": "sound",
                    "playing": sound_running
                }))
                sent_sound = sound_running
        
        # Atualiza tela em 60Hz
        if now - last_display >= 1/60:
            print("here")
            await send_display(ws)
            last_display += 1/60
        # Libera o asyncio
        await asyncio.sleep(0.001)