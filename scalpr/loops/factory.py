import asyncio

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import Mode, Stream
from ..database.database import DataBase
from .producers import candle_producer, historical_candle_producer


class Shared:
    def __init__(self):
        self.shutdown = False
        self.queue = asyncio.Queue()

class CoroFactory:
    """A factory that generates a list of coroutines. Most of them are longrunning processes.
    They all run concurrently.
    """

    def __init__(self, db: DataBase, shared_variables: Shared, client: AsyncClient, manager: BinanceSocketManager):
        self.db = db
        self.mode = db.options.mode
        self.streams = db.options.streams
        self.symbols = db.selected_symbols
        self.shared = shared_variables
        self.manager = manager
        self.client = client


        self.coros = []
        self.add_candle_producers()
        #...
        self.add_historical_candle_producers()

    
    def get_coros(self):
        return self.coros

    
    def add_candle_producers(self):
        if self.mode == Mode.TEST or self.mode == Mode.HISTORY:
            pass
        if Stream.CANDLE not in self.streams:
            pass
        for s in self.symbols:
            coro = candle_producer(s, self.shared, self.manager)
            self.coros.append(coro)


    def add_historical_candle_producers(self):
        if self.mode == Mode.TEST:
            pass
        if Stream.CANDLE not in self.streams:
            pass
        coro = historical_candle_producer(self.shared, self.client, self.db)
        self.coros.append(coro)


