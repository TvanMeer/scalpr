# pylint: disable=no-name-in-module

from datetime import datetime

from pydantic import BaseModel
from pydantic.types import PositiveInt, condecimal


class MiniTicker(BaseModel):
    """24 hour rolling window statistics.

    {
      "e": "24hrMiniTicker",  // Event type
      "E": 123456789,         // Event time
      "s": "BNBBTC",          // Symbol
      "c": "0.0025",          // Close price
      "o": "0.0010",          // Open price
      "h": "0.0025",          // High price
      "l": "0.0010",          // Low price
      "v": "10000",           // Total traded base asset volume
      "q": "18"               // Total traded quote asset volume
    }

    """

    event_time:             datetime                       # E
    current_price:          condecimal(decimal_places=8)   # c
    price_24_hours_ago:     condecimal(decimal_places=8)   # o
    high_price_last_24h:    condecimal(decimal_places=8)   # h
    low_price_last_24h:     condecimal(decimal_places=8)   # l
    base_volume_last_24h:   condecimal(decimal_places=8)   # v
    quote_volume_last_24h:  condecimal(decimal_places=8)   # q


class Ticker(BaseModel):
    """Extended 24 hour rolling window statistics.

       {
        "e": "24hrTicker",  // Event type
        "E": 123456789,     // Event time
        "s": "BNBBTC",      // Symbol
        "p": "0.0015",      // Price change
        "P": "250.00",      // Price change percent
        "w": "0.0018",      // Weighted average price
        "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
        "c": "0.0025",      // Last price
        "Q": "10",          // Last quantity
        "b": "0.0024",      // Best bid price
        "B": "10",          // Best bid quantity
        "a": "0.0026",      // Best ask price
        "A": "100",         // Best ask quantity
        "o": "0.0010",      // Open price
        "h": "0.0025",      // High price
        "l": "0.0010",      // Low price
        "v": "10000",       // Total traded base asset volume
        "q": "18",          // Total traded quote asset volume
        "O": 0,             // Statistics open time
        "C": 86400000,      // Statistics close time
        "F": 0,             // First trade ID
        "L": 18150,         // Last trade Id
        "n": 18151          // Total number of trades
    }


    """

    event_time:                    datetime                       # E
    current_price:                 condecimal(decimal_places=8)   # c
    price_24_hours_ago:            condecimal(decimal_places=8)   # o
    high_price_last_24h:           condecimal(decimal_places=8)   # h
    low_price_last_24h:            condecimal(decimal_places=8)   # l
    weighted_avg_price_last_24h:   condecimal(decimal_places=8)   # w
    price_change_last_24h:         condecimal(decimal_places=8)   # p
    price_change_last_24h_percent: condecimal(decimal_places=3)   # P
    base_volume_last_24h:          condecimal(decimal_places=8)   # v
    quote_volume_last_24h:         condecimal(decimal_places=8)   # q
    n_trades_last_24h:             PositiveInt                    # n
