import asyncio
from typing import List

from binance import AsyncClient, BinanceSocketManager

from ..database.database import DataBase
from ..loops.factory import CoroFactory, Shared
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
        self.db = await self.create_database(options, self.client)
        self.shared = Shared()
        self.tasks = await self.create_tasks(self.db, self.shared, self.client, self.socket_manager)
        _ = await asyncio.gather(*self.tasks)


    async def create_client(self, options: Options) -> AsyncClient:
        return await AsyncClient.create(
            options.key, 
            options.secret, 
            testnet=options.mode == Mode.PAPER
        )


    async def create_database(self, options: Options, client: AsyncClient) -> DataBase:
        db = DataBase(options)
        db = await prepare(options, db, client)
        return db


    async def create_tasks(self, db: DataBase, shared_vars: Shared, client: AsyncClient, manager: BinanceSocketManager) -> List[asyncio.Task]:
        factory = CoroFactory(db, shared_vars, client, manager)
        return factory.get_coros()


    async def shutdown(self):
        print("Shutting down Scalpr in four seconds...")
        self.shared.shutdown = True
        await asyncio.sleep(4)
        await self.client.close_connection()
        print("Scalpr closed gracefully.")
