from decimal import Decimal

from scalpr.database.candle import Candle


def test_candle_init():
    c = Candle(
        open_price=0.0010, 
        close_price=0.0020, 
        high_price=0.0025,
        low_price=0.0015, 
        base_volume=1000,
        quote_volume=1.0000,
        base_volume_taker=500,
        quote_volume_taker=0.500,
        n_trades=100
    )
    assert c.open_price == Decimal("0.001")
