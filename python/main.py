import asyncio #?
import websockets

from elements import chip8, rom
from server_utils.handler import handler
from utils import Logger

logger = Logger()

chip8.load_rom(rom)

async def main():
    logger.log("Servidor iniciando...")
    
    async with websockets.serve(
        handler,
        "0.0.0.0", #?
        8765 #?
    ):
        logger.log("Servidor rodando na porta 8765")
        await asyncio.Future() #?


asyncio.run(main())