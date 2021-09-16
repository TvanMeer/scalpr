from datetime import datetime

from scalpr.database.candle import Candle
from scalpr.database.timeframe import TimeFrame


def test_timeframe_init():
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
    t = TimeFrame(
        open_time=datetime.now(),
        close_time=datetime.now(),
        candle=c
    )
    assert t.candle == c
