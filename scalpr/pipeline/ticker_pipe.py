from typing import Dict

from ..database.ticker import MiniTicker, Ticker
from ..database.window import Window
from .pipe import Pipe


class MiniTickerPipe(Pipe):


    def parse(self, payload: Dict) -> MiniTicker:
        pass

 
    def insert_in_first_timeframe(self, parsed: MiniTicker, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: MiniTicker, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: MiniTicker, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: MiniTicker, window: Window) -> Window:
        pass



class TickerPipe(Pipe):


    def parse(self, payload: Dict) -> Ticker:
        pass

 
    def insert_in_first_timeframe(self, parsed: Ticker, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: Ticker, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: Ticker, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: Ticker, window: Window) -> Window:
        pass
