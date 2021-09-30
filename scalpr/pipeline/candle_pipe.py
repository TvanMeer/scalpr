import logging
from typing import Dict, List

from pydantic import ValidationError

from ..database.candle import Candle
from ..database.window import Window
from .pipe import Message, Pipe


class CandlePipe(Pipe):


    def before(self, message: Message, window: Window) -> Window:
        pass


    def parse(self, payload: Dict) -> Candle:
        try:
            return Candle(
                open_price         =payload["o"],
                close_price        =payload["c"],
                high_price         =payload["h"],
                low_price          =payload["l"],
                base_volume        =payload["v"],
                quote_volume       =payload["q"],
                base_volume_taker  =payload["V"],
                quote_volume_taker =payload["Q"],
                n_trades           =payload["n"],
            )
        except ValidationError as e:
            logging.critical(e)


    def validate(self, message: Message, window: Window) -> bool:
        pass


    def insert_in_previous_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass


class HistoricalCandlePipe(Pipe):


    def before(self, message: Message, window: Window) -> Window:
        pass


    def parse(self, payload: List) -> Candle:
        pass


    def validate(self, message: Message, window: Window) -> bool:
        pass


    def insert_in_first_timeframe(self, message: Message, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass

