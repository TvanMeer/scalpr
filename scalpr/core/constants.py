from enum import Enum


class Mode(str, Enum):
    """Single choice in options.mode."""

    TEST       = "TEST"
    HISTORY    = "HISTORY"
    STREAM     = "STREAM"
    PAPER      = "PAPER"
    TRADE      = "TRADE"


class Stream(str, Enum):
    """Optional multiple choice in options.streams."""

    CANDLE     = "CANDLE"
    MINITICKER = "MINITICKER"
    TICKER     = "TICKER"
    DEPTH5     = "DEPTH5"
    DEPTH10    = "DEPTH10"
    DEPTH20    = "DEPTH20"
    ORDERBOOK  = "ORDERBOOK"
    AGGTRADE   = "AGGTRADE"
    TRADE      = "TRADE"


class Interval(str, Enum):
    """One or multiple choice in options.intervals."""

    SECOND_2   = "2s"
    MINUTE_1   = "1m"
    MINUTE_3   = "3m"
    MINUTE_5   = "5m"
    MINUTE_15  = "15m"
    MINUTE_30  = "30m"
    HOUR_1     = "1h"
    HOUR_2     = "2h"
    HOUR_4     = "4h"
    HOUR_6     = "6h"
    HOUR_8     = "8h"
    HOUR_12    = "12h"
    DAY_1      = "1d"
    DAY_3      = "3d"
    WEEK_1     = "1w"


class ContentType(str, Enum):
    """Different types of content the pipeline can process."""

    CANDLE_STREAM:  "CANDLE_STREAM"
    CANDLE_HISTORY: "CANDLE_HISTORY"


class InTimeFrame(str, Enum):
    """Used in pipeline. 
    Describes in which timeframe a new piece of content should be placed or updated.
    """

    FIRST:    "FIRST"
    PREVIOUS: "PREVIOUS"
    CURRENT:  "CURRENT"
    NEXT:     "NEXT"
    OTHER:    "OTHER"
