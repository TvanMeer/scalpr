import asyncio

from binance import AsyncClient, BinanceSocketManager

from ..database.database import DataBase
from ..options import Options
from .constants import Mode
from .prepare_db import prepare


class Manager:
    """Manages the lifecycle of all coroutines that run concurrently.
    Ensures time synchronization between all producers.
    """

    def __init__(self, options: Options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start(options))


    async def start(self, options: Options):
        self.client = await self.create_client(options)
        self.socket_manager = BinanceSocketManager(self.client)
        self.db = self.create_database(options, self.client)
        #TODO


    async def create_client(self, options: Options):
        return await AsyncClient.create(
            options.key, 
            options.secret, 
            testnet=options.mode == Mode.PAPER
        )


    def create_database(self, options: Options, client: AsyncClient) -> DataBase:
        db = DataBase(options)
        db = prepare(options, db, client)
        return db


    async def shutdown(self):
        await self.client.close_connection()
