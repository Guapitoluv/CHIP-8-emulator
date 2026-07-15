import asyncio #?
import websockets

from elements import chip8
from roms.rom003 import rom
from server_utils.handler import handler

chip8.load_rom(rom)

async def main():
    print("Servidor iniciando...")
    
    async with websockets.serve(
        handler,
        "0.0.0.0", #?
        8765 #?
    ):
        print("Servidor rodando na porta 8765")
        await asyncio.Future() #?


asyncio.run(main())