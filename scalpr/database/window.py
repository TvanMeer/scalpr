# pylint: disable=no-name-in-module

from collections import deque
from typing import Deque

from pydantic import BaseModel

from ..core.constants import Interval
from .timeframe import TimeFrame


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    interval:                   Interval
    timeframes:                 Deque[TimeFrame]    = deque()
