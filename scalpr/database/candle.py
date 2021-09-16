# pylint: disable=no-name-in-module

from pydantic import BaseModel
from pydantic.types import PositiveInt, condecimal


class Candle(BaseModel):
    """Candlestick from websocket stream or historical API call.

    stream:

    {
      "e": "kline",     // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "k": {
        "t": 123400000, // Kline start time
        "T": 123460000, // Kline close time
        "s": "BNBBTC",  // Symbol
        "i": "1m",      // Interval
        "f": 100,       // First trade ID
        "L": 200,       // Last trade ID
        "o": "0.0010",  // Open price
        "c": "0.0020",  // Close price
        "h": "0.0025",  // High price
        "l": "0.0015",  // Low price
        "v": "1000",    // Base asset volume
        "n": 100,       // Number of trades
        "x": false,     // Is this kline closed?
        "q": "1.0000",  // Quote asset volume
        "V": "500",     // Taker buy base asset volume
        "Q": "0.500",   // Taker buy quote asset volume
        "B": "123456"   // Ignore
      }
    }


    history:

    [
      [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
        1499644799999,      // Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "17928899.62484339" // Ignore.
      ]
    ]


    """

    open_price:         condecimal(decimal_places=8, gt=0)  # o   1
    close_price:        condecimal(decimal_places=8, gt=0)  # c   4
    high_price:         condecimal(decimal_places=8, gt=0)  # h   2
    low_price:          condecimal(decimal_places=8, gt=0)  # l   3
    base_volume:        condecimal(decimal_places=8)        # v   5
    quote_volume:       condecimal(decimal_places=8)        # q   7
    base_volume_taker:  condecimal(decimal_places=8)        # V   9
    quote_volume_taker: condecimal(decimal_places=8)        # Q   10
    n_trades:           PositiveInt                         # n   8
    corrupt:            bool = False
