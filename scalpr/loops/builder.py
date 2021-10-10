import asyncio
from abc import ABC, abstractmethod
from typing import List

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import Stream
from . import coro_candle, coro_consumer, coro_user_input
from ..core.state import SharedState


class Builder(ABC):
    """Builds a list with coroutines that are launched concurrently in Manager."""

    @staticmethod
    @abstractmethod
    def user_input_listener(state: SharedState):
        """Build a userinput_listener coroutine."""

    @staticmethod
    @abstractmethod
    def candle_producers(state: SharedState, manager: BinanceSocketManager):
        """Build a websocket stream coroutine for every symbol."""

    @staticmethod
    @abstractmethod
    def historical_candle_producer(state: SharedState, client: AsyncClient):
        """Build one coroutine that downloads candle history for each symbol and time interval."""

    @staticmethod
    @abstractmethod
    def mock_candle_producers(state: SharedState):
        """Build a fake websocket stream coroutine for every symbol."""

    @staticmethod
    @abstractmethod
    def consumer(state: SharedState):
        """Build one coroutine that handles all messages and sends them to their corresponding pipelines."""

    @staticmethod
    @abstractmethod
    def build() -> List[asyncio.Task]:
        """Returns a list of selected coroutines."""



class ConcreteBuilder(Builder):
    """Implementation of builder interface."""

    def __init__(self):
        self.loops = []


    def user_input_listener(self, state: SharedState):
        coro = coro_user_input.user_input_listener(state)
        self.loops.append(coro)
        return self


    def candle_producers(self, state: SharedState, manager: BinanceSocketManager):
        if not Stream.CANDLE in state.db.options.streams:
            return self
        else:
            for s in state.db.selected_symbols:
                coro = coro_candle.candle_producer(state, s, manager)
                self.loops.append(coro)
            return self


    def historical_candle_producer(self, state: SharedState, client: AsyncClient):
        coro = coro_candle.historical_candle_producer(state, client)
        self.loops.append(coro)
        return coro


    def mock_candle_producers(self, state: SharedState):
        if not Stream.CANDLE in state.db.options.streams:
            return self
        else:
            for s in state.db.selected_symbols:
                coro = coro_candle.mock_candle_producer(state, s)
                self.loops.append(coro)
            return self


    def consumer(self, state: SharedState):
        coro = coro_consumer.consumer(state)
        self.loops.append(coro)
        return coro


    def build(self):
        return self.loops
