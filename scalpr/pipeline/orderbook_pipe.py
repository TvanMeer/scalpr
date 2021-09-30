# pylint: disable=no-name-in-module

from typing import Dict, List, Union

from pydantic import BaseModel

from ..database.orderbook import OrderBookUpdate
from ..database.window import Window
from .pipe import Message, Pipe


class OrderbookPipe(Pipe):


    def before(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    def parse(self, payload: Union[Dict, List]) -> BaseModel:
        raise NotImplementedError

    def validate(self, message: Message, window: Window) -> bool:
        raise NotImplementedError

    def insert_in_previous_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    def insert_in_current_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    def insert_in_next_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError
