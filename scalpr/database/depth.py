# pylint: disable=no-name-in-module

from collections import deque
from datetime import datetime
from typing import Deque, Tuple

from pydantic import BaseModel


class Bid(BaseModel):
    price:    float
    quantity: float


class Ask(BaseModel):
    price:    float
    quantity: float

class Depth(BaseModel):
    """Depthchart, showing the best bids and asks in the orderbook.
    orders[0] is the best bid and ask, orders[1] the second best etc.
    The orders are a snapshot of the depthcache at close time of the timeframe.

    The value Options._depthcache_size represents the number of orders saved
    in Depth.orders.
    E.g. if Options._depthcache_size is equal to 5, the top 5 best bids and asks
    will be saved in Depth.orders.
    """

    orders:            Deque[Tuple[Bid, Ask]] = deque()
    last_update_time:  datetime
