from dataclasses import dataclass

from .constants import Interval


@dataclass
class UserInput:
    shutdown:    bool     = False
    get_db:      bool     = False
    symbol:      str      = None
    window:      Interval = None
    timeframe:   int      = None
    as_datatype: str      = "nested_class"
