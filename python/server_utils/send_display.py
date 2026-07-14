import json

from elements import chip8

async def send_display(ws):
    #print("pixels ligados:", sum(chip8.display.pixels))
    await ws.send(json.dumps({
        "type": "display",
        "pixels": chip8.display.pixels.tolist()
    }))