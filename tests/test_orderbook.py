# pylint: disable=no-name-in-module

from scalpr.database.orderbook import Ask, Bid, OrderBookUpdate


def test_orderbookupdate_init():
    b = Bid(
        price=4.00000000, 
        quantity=431.00000000
    )
    a = Ask(
        price=4.00000200,
        quantity=12.00000000
    )
    o = OrderBookUpdate(
        update_id=1027024,
    )
    o.bids.append(b)
    o.asks.append(a)
    assert o.update_id == 1027024
    assert o.bids[0] == b
    assert o.asks[0] == a
