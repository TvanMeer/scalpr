from typing import Dict, Set

from binance.client import AsyncClient

from ..database.database import DataBase
from ..database.symbol import Symbol
from ..options import Options


async def download_exchange_info(client: AsyncClient) -> Dict:
    return await client.get_exchange_info()


def select_symbols(exchange_info: Dict, options: Options) -> Set[str]:
    selected = set()
    for s in exchange_info["symbols"]:
        b = s["baseAsset"] in options.base_assets or options.base_assets == {"*"}
        q = s["quoteAsset"] in options.quote_assets or options.quote_assets == {"*"}
        a = bool(s["isSpotTradingAllowed"])
        if b and q and a:
            selected.add(s["symbol"])
    return selected


def add_symbols(selected_symbols: Set[str], db: DataBase):
    db.selected_symbols = selected_symbols
    for s in selected_symbols:
        db.symbols[s] = Symbol(name=s)
    return db
    

async def prepare(options: Options, db: DataBase, client: AsyncClient) -> DataBase:
    info = await download_exchange_info(client)
    selected_symbols = select_symbols(info, options)
    db = add_symbols(selected_symbols, db)
    client.close_connection()
    return db





