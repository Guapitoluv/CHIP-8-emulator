import asyncio
import json

from elements import chip8, debugger, emulator_server
from roms.rom003 import rom
from models.message import WaitingKeyMsg, PressedKeyMsg, DisplayMsg, ResetMsg

def parseMsg(data):
    if "type" not in data: return
    
    match data["type"]:
        case "waiting_key": return WaitingKeyMsg()
        case "pressedkey": return PressedKeyMsg(data["key"])
        case "sound": return SoundMsg(data["playing"])
        case "display": return DisplayMsg(data["pixesl"])
        case "reset": return ResetMsg()
        

async def handler(ws):
    print("Cliente conectado")
    try:
        chip8.running = True
        
        task = asyncio.create_task(emulator_server.emulator_loop(ws))

        try:
            async for message in ws:
                data = json.loads(message)
                print("data:", data)
                msg = parseMsg(data)
                print("msg:", msg)
                
                match msg.type:
                    case "pressedkey":
                        chip8.keyboard.press(int(msg.key, 16));
                
                    case "reset":
                        print("received reset")
                        chip8.reset()
                        #print(hex(debugger.peek_opcode()))
                        chip8.load_rom(rom)
                        #print(hex(debugger.peek_opcode()))
                        await DisplayMsg(chip8.display.pixels.tolist()).send(ws)
                        #print("reseted")
        
        finally:
            print("finali")
            task.cancel()
    
    except Exception as e:
        print(e)
    
    finally:
        print("final")
        chip8.running = False
        task.cancel()