from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from ..options import Options


class TreeElement():
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

@dataclass
class Candle(Leaf):
    """Candle data that spawns the time interval of the parent timeframe."""

    open_price:              Decimal
    close_price:             Decimal
    high_price:              Decimal
    low_price:               Decimal
    base_volume:             Decimal
    quote_volume:            Decimal


@dataclass
class Ticker(Leaf):
    """24 hour rolling average ticker data that spawns the time interval 
    of the parent timeframe.
    """

    open_price_rolling24h:   Decimal
    close_price_rolling24h:  Decimal
    high_price_rolling24h:   Decimal
    low_price_rolling24h:    Decimal
    base_volume_rolling24h:  Decimal
    quote_volume_rolling24h: Decimal


@dataclass
class Trade(Leaf):
    """Single trade."""

    _id:      int
    time:     datetime
    price:    Decimal
    quantity: Decimal
    is_taker: bool


@dataclass
class Bid(Leaf):
    price:    Decimal
    quantity: Decimal
    cumsum:   Decimal

@dataclass
class Ask(Leaf):
    price:    Decimal
    quantity: Decimal
    cumsum:   Decimal

@dataclass
class OrderBookAtOpen(Leaf):
    """The orderbook/ depthchart at open time of candle."""

    depth:    int
    bids:     list[Bid] = []
    asks:     list[Ask] = []

@dataclass
class OrderBookUpdate(Leaf):
    """An update of the orderbook."""

    update_id: int
    is_bid:    bool
    data:      Bid | Ask


@dataclass
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
    trades:            deque[Trade]            = deque()
    orderbook_updates: deque[OrderBookUpdate]  = deque()


@dataclass
class Window(Branch):
    """Window that holds all candles of a specific time interval.
    The orderbook is optional.
    """

    interval:                  timedelta
    timeframes:                deque           = deque()
    orderbook_at_first_candle: OrderBookAtOpen = OrderBookAtOpen(depth=0)


@dataclass
class Symbol(Branch):
    """Container that holds all windows for a specific symbol."""

    name:                   str
    windows:                dict[str, Window]  = {}
    ticker:                 Optional[Ticker]   = None


@dataclass
class Data(Branch):
    """The root container that holds all realtime data."""

    options:                 Options
    symbols:                 dict[str, Symbol] = {}
    all_symbols_at_exchange: set[str]          = set()
