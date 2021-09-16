# pylint: disable=no-name-in-module

from collections import deque
from datetime import datetime
from typing import Deque, Optional, Union

from pydantic import BaseModel

from .candle import Candle
from .depth import Depth5, Depth10, Depth20
from .orderbook import OrderBookUpdate
from .ticker import MiniTicker, Ticker
from .trade import AggTrade, Trade


class TimeFrame(BaseModel):
    """Contains all data related to market events between two points in time.

    Candle covers this timeframe and is updated until this timeframe is closed.
    The other fields are updated until this timeframe is closed.
    """

    open_time:          datetime
    close_time:         datetime

    candle:             Optional[Candle]                          = None
    miniticker:         Optional[MiniTicker]                      = None
    ticker:             Optional[Ticker]                          = None
    depth:              Optional[Union[Depth5, Depth10, Depth20]] = None
    orderbook_updates:  Deque[OrderBookUpdate]                    = deque()
    aggtrades:          Deque[AggTrade]                           = deque()
    trades:             Deque[Trade]                              = deque()
