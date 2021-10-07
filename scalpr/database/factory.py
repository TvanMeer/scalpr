from typing import Dict, Set

from binance.client import AsyncClient

from ..options import Options
from .database import DataBase
from .symbol import Symbol
from .window import Window


class DatabaseFactory:
    """Factory that creates a DataBase instance.
    Downloads exchange info and selects tradable symbols.
    Initializes nested objects within the database.
    """
    
    async def create_database(self, options: Options, client: AsyncClient) -> DataBase:
        """Client function that should be called to create a DataBase instance."""
        
        db = DataBase(options)
        info = await client.get_exchange_info()
        selected = self.select_symbols(info, options)
        db = self.add_symbols(selected, db)
        db = self.add_windows(db)
        return db


    def select_symbols(self, exchange_info: Dict, options: Options) -> Set[str]:
        selected = set()
        for s in exchange_info["symbols"]:
            b = s["baseAsset"] in options.base_assets or options.base_assets == {"*"}
            q = s["quoteAsset"] in options.quote_assets or options.quote_assets == {"*"}
            a = bool(s["isSpotTradingAllowed"])
            if b and q and a:
                selected.add(s["symbol"])
        return selected


    def add_symbols(self, selected_symbols: Set[str], db: DataBase) -> DataBase:
        db.selected_symbols = selected_symbols
        for s in selected_symbols:
            db.symbols[s] = Symbol(name=s)
        return db


    def add_windows(self, db: DataBase) -> DataBase:
        for s in db.symbols:
            for iv in db.options.window_intervals:
                db.symbols[s].windows[iv] = Window(interval=iv)
        return db
