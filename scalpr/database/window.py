# pylint: disable=no-name-in-module

from collections import deque
from typing import Deque, Optional

from pydantic import BaseModel

from ..core.constants import Interval
from .candle import Candle
from .timeframe import TimeFrame


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    interval:                   Interval
    timeframes:                 Deque[TimeFrame]    = deque()

    _last_candle_update:        Optional[Candle]    = None
    _last_candle_update_closed: Optional[bool]      = None
    _history_downloaded:        bool                = False
