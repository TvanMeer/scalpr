# pylint: disable=no-name-in-module


from typing import Dict, List, Union

from pydantic import BaseModel

from ..database.trade import AggTrade, Trade
from ..database.window import Window
from .pipe import Message, Pipe


class AggTradePipe(Pipe):


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



class TradePipe(Pipe):


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
