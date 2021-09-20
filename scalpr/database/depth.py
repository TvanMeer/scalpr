# pylint: disable=no-name-in-module

from collections import deque
from typing import Deque

from pydantic import BaseModel


class Bid(BaseModel):
    price:    float
    quantity: float


class Ask(BaseModel):
    price:    float
    quantity: float

class Depth(BaseModel):
    """Depthcache, showing the best bids and asks in the orderbook.
    Timeframe.depth.bids[0] is the best bid, Timeframe.depth.bids[1] 
    the second best etc.
    The bids and asks are a snapshot of the depthcache at close time 
    of the timeframe.

    The value Options._depthcache_size represents the number of bids 
    and asks saved.
    E.g. if Options._depthcache_size is equal to 5, 
    the top 5 best bids and asks will be saved.
    """

    bids:  Deque[Bid]  = deque()
    asks:  Deque[Ask]  = deque()
