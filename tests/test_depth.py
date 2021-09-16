from datetime import datetime
from decimal import Decimal

from scalpr.database.depth import Depth5


def test_depth_init():
    d = Depth5(
        last_update_time = datetime.now(),
        bid1= (45724.66000000, 0.00000000),
        ask1= (45720.40000000, 2.66240200),
        bid2= (45724.66000000, 0.00000000),
        ask2= (45720.40000000, 2.66240200),
        bid3= (45724.66000000, 0.00000000),
        ask3= (45720.40000000, 2.66240200),
        bid4= (45724.66000000, 0.00000000),
        ask4= (45720.40000000, 2.66240200),
        bid5= (45724.66000000, 0.00000000),
        ask5= (45720.40000000, 2.66240200)
    )

    assert d.bid1 == (Decimal('45724.66'), Decimal('0.0'))
