from typing import Dict

from ..core.constants import InTimeFrame
from ..database.candle import Candle
from ..database.window import Window
from .pipe import Pipe


class CandlePipe(Pipe):

        
    def which_timeframe(self, payload: Dict, window: Window) -> InTimeFrame:
        pass


    def parse(self, payload: Dict) -> Candle:
        pass

 
    def insert_in_first_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass


    def insert_in_previous_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass


    def insert_in_current_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass

    
    def insert_in_next_timeframe(self, parsed: Candle, window: Window) -> Window:
        pass
