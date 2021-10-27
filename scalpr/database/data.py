from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Optional, Set, TypeVar

from pydantic import BaseModel, condecimal, constr

from ..options import Options

LargeNum = TypeVar("LargeNum", bound=condecimal(decimal_places=8, gt=0))


class TreeElement(BaseModel):
    """All realtime data is merged in a tree, with the following nested structure:
    
    Data
       Symbol[]
          Window[]
             Candle
             Trade[]
             OrderBookAtOpen
             OrderBookUpdate[]
    """
    ...


class Branch(TreeElement):
    ...

class Leaf(TreeElement):
    ...


class Candle(Leaf):
    """Candle data that spawns the time interval of the parent timeframe."""

    open_price:              LargeNum
    close_price:             LargeNum
    high_price:              LargeNum
    low_price:               LargeNum
    base_volume:             LargeNum
    quote_volume:            LargeNum


class Ticker(Leaf):
    """24 hour rolling average ticker data that spawns the time interval 
    of the parent timeframe.
    """

    open_price_rolling24h:   LargeNum
    close_price_rolling24h:  LargeNum
    high_price_rolling24h:   LargeNum
    low_price_rolling24h:    LargeNum
    base_volume_rolling24h:  LargeNum
    quote_volume_rolling24h: LargeNum


class Trade(Leaf):
    """Single trade."""

    _id:      int
    time:     datetime
    price:    LargeNum
    quantity: LargeNum
    is_taker: bool


class Bid(Leaf):
    price:          LargeNum
    quantity:       LargeNum
    cumulative_sum: LargeNum

class Ask(Leaf):
    price:          LargeNum
    quantity:       LargeNum
    cumulative_sum: LargeNum

class OrderBookAtOpen(Leaf):
    """The orderbook/ depthchart at open time of candle."""

    depth:    int
    bids:     List[Bid] = []
    asks:     List[Ask] = []

class OrderBookUpdate(Leaf):
    """An update of the orderbook."""

    update_id: int
    is_bid:    bool
    data:      Bid | Ask


class TimeFrame(Branch):
    """Timeframe that holds:
     -candle data
     -trade data
     -orderbook data
     -ticker data

     All content types are optional.

     """

    open_time:         datetime
    close_time:        datetime

    candle:            Optional[Candle]        = None
    ticker:            Optional[Ticker]        = None
    trades:            Deque[Trade]            = deque()
    orderbook_updates: Deque[OrderBookUpdate]  = deque()


class Window(Branch):
    """Window that holds all candles of a specific time interval.
    The orderbook is optional.
    """

    interval:                  timedelta
    timeframes:                Deque           = deque()
    orderbook_at_first_candle: OrderBookAtOpen = OrderBookAtOpen(depth=0)


class Symbol(Branch):
    """Container that holds all windows for a specific symbol."""

    name:    constr(min_length=3, max_length=8)
    windows: Dict[str, Window]                 = {}
    ticker:  Optional[Ticker]                  = None


class Data(Branch):
    """The root container that holds all realtime data."""

    options:                 Options
    symbols:                 Dict[str, Symbol] = {}
    all_symbols_at_exchange: Set[str]          = set()
