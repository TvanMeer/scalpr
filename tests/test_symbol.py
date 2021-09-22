from scalpr.database.symbol import Symbol


def test_symbol_init():
    s = Symbol(name="BTC")
    assert s.name == "BTC"
    assert isinstance(s.windows, dict)
