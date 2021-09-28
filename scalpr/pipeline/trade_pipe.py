from typing import Dict

from ..database.trade import AggTrade, Trade
from ..database.window import Window
from .pipe import Pipe


class AggTradePipe(Pipe):


    def parse(self, payload: Dict) -> AggTrade:
        pass

 
    def insert_in_first_timeframe(self, parsed: AggTrade, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: AggTrade, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: AggTrade, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: AggTrade, window: Window) -> Window:
        pass



class TradePipe(Pipe):


    def parse(self, payload: Dict) -> Trade:
        pass

 
    def insert_in_first_timeframe(self, parsed: Trade, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: Trade, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: Trade, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: Trade, window: Window) -> Window:
        pass
