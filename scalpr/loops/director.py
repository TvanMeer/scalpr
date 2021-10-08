from abc import ABC, abstractmethod
from asyncio import Task
from typing import List

from binance import AsyncClient, BinanceSocketManager

from .builder import ConcreteBuilder
from .state import SharedState


class Director(ABC):

    @staticmethod
    @abstractmethod
    def construct(state: SharedState, client: AsyncClient = None, manager: BinanceSocketManager = None) -> List[Task]:
        """Constructs all coroutines that run concurrently."""


class TestDirector(Director):
    @staticmethod
    def construct(state: SharedState) -> List[Task]:
        return ConcreteBuilder()\
            .consumer(state)\
            .user_input_listener(state)\
            .mock_candle_producers(state)\
            .build()


class HistoryDirector(Director):
    @staticmethod
    def construct(state: SharedState, client: AsyncClient) -> List[Task]:
        return ConcreteBuilder()\
            .consumer(state)\
            .user_input_listener(state)\
            .historical_candle_producer(state, client)\
            .build()


class StreamDirector(Director):
    @staticmethod
    def construct(state: SharedState, client: AsyncClient, manager: BinanceSocketManager) -> List[Task]:
        return ConcreteBuilder()\
            .consumer(state)\
            .user_input_listener(state)\
            .candle_producers(state, manager)\
            .historical_candle_producer(state, client)\
            .build()


class PaperDirector(Director):
    @staticmethod
    def construct(state: SharedState, client: AsyncClient, manager: BinanceSocketManager) -> List[Task]:
        return ConcreteBuilder()\
            .consumer(state)\
            .user_input_listener(state)\
            .candle_producers(state, manager)\
            .historical_candle_producer(state, client)\
            .build()


class TradeDirector(Director):
    @staticmethod
    def construct(state: SharedState, client: AsyncClient, manager: BinanceSocketManager) -> List[Task]:
        return ConcreteBuilder()\
            .consumer(state)\
            .user_input_listener(state)\
            .candle_producers(state, manager)\
            .historical_candle_producer(state, client)\
            .build()
