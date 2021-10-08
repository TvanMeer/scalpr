import asyncio
from queue import Queue
from typing import List

from binance import AsyncClient, BinanceSocketManager

from ..database.factory import DatabaseFactory
from ..loops.director import (Director, HistoryDirector, PaperDirector,
                              StreamDirector, TestDirector, TradeDirector)
from ..loops.state import SharedState
from ..options import Options
from .constants import Mode


class Manager:
    """Manages the lifecycle of all coroutines that run concurrently.
    Ensures time synchronization between all producers.
    """

    def start(self, options: Options, userinput_queue: Queue):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_async(options, userinput_queue))



    async def start_async(self, options: Options, userinput_queue: Queue):
        client = await self.create_client(options)
        socket_manager = BinanceSocketManager(client)
        db_factory = DatabaseFactory()
        database = await db_factory.create_database(options, client)
        state = SharedState(database, userinput_queue)
        director = self.create_loops_director(options)
        loops = self.create_loops(state, director, client, socket_manager)
        _ = await asyncio.gather(*loops)
        await client.close_connection()



    async def create_client(self, options: Options) -> AsyncClient:
        return await AsyncClient.create(
            options.key, 
            options.secret, 
            testnet=options.mode == Mode.PAPER
        )



    def create_loops_director(self, options: Options) -> Director:
        directors = {
            Mode.TEST:    TestDirector,
            Mode.HISTORY: HistoryDirector,
            Mode.STREAM:  StreamDirector,
            Mode.PAPER:   PaperDirector,
            Mode.TRADE:   TradeDirector
        }
        return directors[options.mode]



    def create_loops(self, state: SharedState, director: Director, client: AsyncClient, manager: BinanceSocketManager) -> List[asyncio.Task]:
        if director is TestDirector:
            return TestDirector.construct(state)
        if director is HistoryDirector:
            return HistoryDirector.construct(state, client)
        return director.construct(state, client, manager)
