# pylint: disable=no-name-in-module

from typing import Dict, Set

from pydantic import BaseModel

from ..options import Options
from .symbol import Symbol


class DataBase(BaseModel):
    """The root of the datamodel.
    This class is injected in user defined feature functions.
    All data is nested in this model, hierarchically:

    db -> dict[str, Symbol] -> dict[Options.Interval, Window] -> deque[Timeframe] -> candle
                                                                                  -> miniticker
                                                                                  -> ...

    Database contains one or more symbols, like `btcusdc` and `ethbtc`.
    A symbol contains one or more windows, like `1m` and `4h`.
    A window contains a sequence of timeframes.

    A timeframe contains one candle, 
    one miniticker at close time, 
    one ticker at close time, 
    the depth cache at close time,
    all orderbook updates within the timeframe,
    all trades within the timeframe, and
    all aggregate trades within the timeframe.

    Example:
    Get last 1 minute candle for symbol `BTCUSDC`:

    db.symbols["btcusdc"].windows[Interval.minute_1].timeframes[-1].candle
    """

    options:          Options
    selected_symbols: Set[str] = set()
    # exchange info
    # account info

    symbols:          Dict[str, Symbol] = dict()
    # user events
