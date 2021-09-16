# pylint: disable=no-name-in-module

from collections import deque
from typing import Deque

from pydantic import BaseModel
from pydantic.types import PositiveInt, condecimal


class Bid(BaseModel):
    price:    condecimal(decimal_places=8, gt=0)
    quantity: condecimal(decimal_places=8, gt=0)


class Ask(BaseModel):
    price:    condecimal(decimal_places=8, gt=0)
    quantity: condecimal(decimal_places=8, gt=0)


class OrderBook(BaseModel):
    """Orderbook updates within timeframe.

    {
      "lastUpdateId": 1027024,
      "bids": [
        [
          "4.00000000",     // PRICE
          "431.00000000"    // QTY
        ]
      ],
      "asks": [
        [
          "4.00000200",
          "12.00000000"
        ]
      ]
    }

    """

    update_id: PositiveInt
    bids:      Deque[Bid]   = deque()
    asks:      Deque[Ask]   = deque()
