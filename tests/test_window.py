from scalpr.core.constants import Interval
from scalpr.database.window import Window


def test_window_init():
    w = Window(interval=Interval("1m"))
    assert w.interval == Interval("1m")
