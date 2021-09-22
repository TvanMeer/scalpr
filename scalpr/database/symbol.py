# pylint: disable=no-name-in-module

from typing import Dict

from pydantic import BaseModel
from pydantic.types import constr

from ..core.constants import Interval
from .window import Window


class Symbol(BaseModel):
    """Holds all data related to a symbol, such as `BTCUSDT`."""

    name:    constr(strip_whitespace=True, min_length=3, max_length=12)
    windows: Dict[Interval, Window] = dict()
