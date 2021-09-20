from datetime import datetime

from scalpr.database.depth import Ask, Bid, Depth
from scalpr.database.timeframe import TimeFrame


def test_depth_init():
    
    bid = Bid(price=0.123, quantity=12.01)
    ask = Ask(price=0.125, quantity=10.47)
    depth = Depth()
    depth.bids.append(bid)
    depth.asks.append(ask)

    ot = datetime.now()
    ct = datetime.now()
    timeframe = TimeFrame(open_time=ot, close_time=ct)
    timeframe.depth = depth

    assert timeframe.depth.bids[0].price == 0.123
    assert timeframe.depth.asks[0].price == 0.125
