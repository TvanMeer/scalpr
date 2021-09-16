# pylint: disable=no-name-in-module

from typing import Tuple
from datetime import datetime

from pydantic import BaseModel
from pydantic.types import condecimal


class Depth5(BaseModel):
    """Depthchart, showing the best bids and asks in the orderbook.
    Bid1 is the best bid, bid2 the second best.
    Ask1 is the best ask, ask2 the second best etcetera.

    Every entry is a tuple of <price, quantity>
    """

    last_update_time: datetime    
    bid1:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask1:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid2:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask2:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid3:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask3:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid4:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask4:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid5:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask5:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]

class Depth10(Depth5):
    bid6:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask6:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid7:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask7:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid8:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask8:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid9:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask9:  Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid10: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask10: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]

class Depth20(Depth10):
    bid11: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask11: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid12: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask12: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid13: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask13: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid14: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask14: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid15: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask15: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid16: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask16: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid17: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask17: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid18: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask18: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid19: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask19: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    bid20: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]
    ask20: Tuple[condecimal(decimal_places=8), condecimal(decimal_places=8)]