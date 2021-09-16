# pylint: disable=no-name-in-module

from datetime import datetime

from pydantic import BaseModel
from pydantic.types import PositiveInt, StrictBool, condecimal


class AggTrade(BaseModel):
    """Aggregate trade: trade information that is aggregated for a single taker order.

        {
      "e": "aggTrade",  // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "a": 12345,       // Aggregate trade ID
      "p": "0.001",     // Price
      "q": "100",       // Quantity
      "f": 100,         // First trade ID
      "l": 105,         // Last trade ID
      "T": 123456785,   // Trade time
      "m": true,        // Is the buyer the market maker?
      "M": true         // Ignore
    }

    """

    trade_time:          datetime
    aggtrade_id:         PositiveInt
    first_trade_id:      PositiveInt
    last_trade_id:       PositiveInt
    price:               condecimal(decimal_places=8)
    quantity:            condecimal(decimal_places=8)
    buyer_is_maker:      StrictBool


class Trade(BaseModel):
    """Raw information about a single (partial) trade/transaction. 
    Each trade has a unique buyer and seller.

        {
      "e": "trade",     // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "t": 12345,       // Trade ID
      "p": "0.001",     // Price
      "q": "100",       // Quantity
      "b": 88,          // Buyer order ID
      "a": 50,          // Seller order ID
      "T": 123456785,   // Trade time
      "m": true,        // Is the buyer the market maker?
      "M": true         // Ignore
    }


    """

    trade_time:          datetime
    trade_id:            PositiveInt
    buyer_order_id:      PositiveInt
    seller_order_id:     PositiveInt
    price:               condecimal(decimal_places=8)
    quantity:            condecimal(decimal_places=8)
    buyer_is_maker:      StrictBool
