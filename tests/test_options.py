# pylint: disable=no-name-in-module

import pytest
from pydantic.error_wrappers import ValidationError
from scalpr.core.constants import Interval, Mode, Stream
from scalpr.options import Options


@pytest.fixture()
def valid_credential():
    # Fake
    return "nsfXDBT5fTeYJX3QXECFyHzkQJfznfhY62bSI8AVYT4ITdofNbcImikj3tZVWUig"

def test_init():
    o = Options()
    assert o.key == " "
    assert o.mode == Mode.TEST


def test_check_credentials(valid_credential):
    o = Options(key=valid_credential, secret=valid_credential)
    assert o.key == o.secret == valid_credential

    o = Options(key=" ", secret=" ")
    assert o.key == o.secret == " "

    with pytest.raises(ValidationError):
        Options(key="foo", secret="bar")
    

def test_datadir():
    Options(datadir="/home/")
    with pytest.raises(ValidationError):
        Options(datadir="foo")

@pytest.mark.parametrize("asset", ["BTC", ["HOT", "DONUT"]])
def test_check_asset_names_valid(asset):
    o = Options(base_assets=asset)
    if asset == "BTC":
        assert o.base_assets == {"BTC"}
    else:
        assert o.base_assets == {"HOT", "DONUT"}


@pytest.mark.parametrize("asset", ["BT", ["HOT", "DONUTxxxxxxx"], "BT?"])
def test_check_asset_names_invalid(asset):
    with pytest.raises(ValidationError):
        Options(base_assets=asset)


def test_make_window_intervals():
    o = Options(window_intervals="1m")
    assert o.window_intervals == {Interval.MINUTE_1}

    with pytest.raises(ValidationError):
        Options(window_intervals="foo")

    o = Options(window_intervals=["2s", "1m"])
    assert o.window_intervals == {Interval.SECOND_2, Interval.MINUTE_1}

    with pytest.raises(ValidationError):
        Options(window_intervals=123)


def test_check_window_length():
    o = Options(window_length="*")
    assert o.window_length == 0

    o = Options(window_length=1000)
    assert o.window_length == 1000

    with pytest.raises(ValidationError):
        Options(window_length=-1)

    with pytest.raises(ValidationError):
        Options(window_length="foo")


def test_make_streams():
    o = Options(streams="candle")
    assert o.streams == {Stream.CANDLE}

    with pytest.raises(ValidationError):
        Options(streams="foo")

    o = Options(streams=["candle", "trade"])
    assert o.streams == {Stream.CANDLE, Stream.TRADE}

    with pytest.raises(ValidationError):
        Options(streams=["candle", "foo"])

    with pytest.raises(ValidationError):
        Options(streams=123)

    o = Options(streams="depth125")
    assert o.streams == {Stream.DEPTH}
    assert o._depthcache_size == 125
