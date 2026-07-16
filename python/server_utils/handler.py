import asyncio
import json

from elements import chip8, debugger, emulator_server, rom
from models.message import WaitingKeyMsg, PressedKeyMsg, DisplayMsg, ResetMsg, ReleasedKeyMsg
from errors import InvalidMsgTypeError, InvalidMsgFormatError
from utils import Logger

logger = Logger()

def parseMsg(data):
    if "type" not in data:
        raise InvalidMsgFormatError(data)
    
    match data["type"]:
        case "waiting_key": return WaitingKeyMsg()
        case "pressedkey": return PressedKeyMsg(data["key"])
        case "releasedkey": return ReleasedKeyMsg(data["key"])
        case "sound": return SoundMsg(data["playing"])
        case "display": return DisplayMsg(data["pixels"])
        case "reset": return ResetMsg()
        case _: raise InvalidMsgTypeError(data["type"])
        

async def handler(ws):
    logger.log("Cliente conectado")
    try:
        chip8.running = True
        
        task = asyncio.create_task(emulator_server.emulator_loop(ws))

        try:
            async for message in ws:
                data = json.loads(message)
                try:
                    msg = parseMsg(data)
                except InvalidMsgTypeError as e:
                    logger.log(e)
                    continue
                
                match msg.type:
                    case "pressedkey":
                        logger.log("pressed")
                        chip8.keyboard.press(int(msg.key, 16));
                    
                    case "releasedkey":
                        logger.log("released")
                        chip8.keyboard.release(int(msg.key, 16));
                    
                    case "reset":
                        logger.log("received reset")
                        chip8.reset()
                        chip8.load_rom(rom)
                        
                        await DisplayMsg(chip8.display.pixels.tolist()).send(ws)
                    
                    case _:
                        logger.log("Unknown message:", msg.type)
        
        finally:
            logger.log("final I")
            task.cancel()
    
    except Exception as e: logger.log(e)
    
    finally:
        logger.log("final II")
        chip8.running = False
        task.cancel()