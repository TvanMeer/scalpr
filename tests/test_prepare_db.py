import pytest
from binance.client import AsyncClient
from scalpr.core.prepare_db import (add_symbols, download_exchange_info,
                                    prepare, select_symbols)
from scalpr.database.database import DataBase
from scalpr.database.symbol import Symbol
from scalpr.options import Options


@pytest.fixture
def options():
    return Options()

@pytest.fixture
def db(options):
    return DataBase(options=options)

@pytest.fixture
async def client():
    return AsyncClient()

@pytest.fixture
async def exchange_info(client):
    return await client.get_exchange_info()

@pytest.mark.asyncio
async def test_download_exchange_info(client):
    info = await download_exchange_info(client)
    assert len(info["symbols"]) >= 1648

def test_select_symbols(exchange_info, options):
    options.base_assets = {"BTC", "XRP"}
    options.quote_assets = {"USDT"}
    selected = select_symbols(exchange_info, options)
    assert "BTCUSDT" in selected
    assert "XRPUSDT" in selected
    assert len(selected) == 2

def test_add_symbols(db):
    selected = {"BTCUSDT", "XRPUSDT"}
    updated_db = add_symbols(selected, db)
    assert updated_db.selected_symbols == selected
    assert updated_db.symbols["BTCUSDT"] == Symbol(name="BTCUSDT")

@pytest.mark.asyncio
async def test_prepare(options, db, client):
    options.base_assets = {"BTC", "XRP"}
    options.quote_assets = {"USDT"}
    updated_db = await prepare(options, db, client)
    assert updated_db.selected_symbols == {"BTCUSDT", "XRPUSDT"}

