from datetime import datetime
from decimal import Decimal

from scalpr.database.trade import AggTrade, Trade


def test_aggtrade_init():
    t = AggTrade(
        trade_time=datetime.now(),
        aggtrade_id=12345,
        first_trade_id=100,
        last_trade_id=105,
        price=0.001,
        quantity=100,
        buyer_is_maker=True
    )
    assert t.price == Decimal("0.001")

def test_trade_init():
    t = Trade(
        trade_time = datetime.now(),
        trade_id=12345,
        buyer_order_id=88,
        seller_order_id=50,
        price=0.001,
        quantity=100,
        buyer_is_maker=True
    )
    assert t.price == Decimal("0.001")
