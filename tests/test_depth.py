from datetime import datetime

from scalpr.database.depth import Ask, Bid, Depth


def test_depth_init():
    order_1 = (
        Bid(price=0.123, quantity=12.01), 
        Ask(price=0.125, quantity=10.47)
    )
    time = datetime.now()
    d = Depth(last_update_time=time)
    d.orders.append(order_1)
    assert d.orders[0][0].price == 0.123
    assert d.orders[0][1].price == 0.125
