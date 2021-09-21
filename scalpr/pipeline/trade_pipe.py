from typing import Dict

from ..core.constants import InTimeFrame
from ..database.trade import AggTrade, Trade
from ..database.window import Window
from .pipe import Pipe


class AggTradePipe(Pipe):

        
    def which_timeframe(self, payload: Dict, window: Window) -> InTimeFrame:
        pass


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

        
    def which_timeframe(self, payload: Dict, window: Window) -> InTimeFrame:
        pass


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
