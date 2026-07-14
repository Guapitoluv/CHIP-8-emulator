import asyncio
import json

from elements import chip8
from server_utils.emulator_loop import emulator_loop
from server_utils.send_display import send_display
from roms.rom003 import rom

async def handler(ws):
    print("Cliente conectado")
    try:
        chip8.running = True
        
        task = asyncio.create_task(emulator_loop(ws))

        try:
            async for message in ws:
                data = json.loads(message)
                
                if "type" in data: print(data["type"])
                
                if data["type"] == "pressedkey":
                    if "key" in data:
                        print("received pressedkey")
                        chip8.keyboard.press(int(data["key"], 16));
                
                if data["type"] == "restart":
                    print("received reset")
                    chip8.reset()
                    chip8.load_rom(rom)
                    #await send_display(ws)
                    print("reseted")
        
        finally:
            print("finalii")
            task.cancel()
    
    except Exception as e:
        print(e)
    
    finally:
        print("final")
        chip8.running = False
        task.cancel()