from datetime import datetime
from decimal import Decimal

from scalpr.database.ticker import MiniTicker


def test_miniticker_init():
    m = MiniTicker(
        event_time= datetime.now(),
        current_price=0.0025,
        price_24_hours_ago=0.0010,
        high_price_last_24h=0.0025,
        low_price_last_24h=0.0010,
        base_volume_last_24h=10000,
        quote_volume_last_24h=18
    )

    assert m.current_price == Decimal('0.0025')
