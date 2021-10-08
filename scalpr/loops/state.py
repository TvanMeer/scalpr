import asyncio
from dataclasses import dataclass, field
from queue import Queue
from typing import Dict

from ..database.database import DataBase


@dataclass
class SharedState:
    """Holds data that is shared between all concurrent loops.
    Contains both state variables for internal usage, and
    the database instance.
    """

    db:                         DataBase
    stop:                       bool          = False
    queue:                      asyncio.Queue = asyncio.Queue()
    user_input_queue:           Queue         = Queue()
    history_downloaded:         Dict          = field(init=False)
    last_candles_update:        Dict          = field(init=False)
    last_candles_update_closed: Dict          = field(init=False)


    def __post_init__(self):
        self.history_downloaded = self.init_history_downloaded(self.db)
        self.last_candles_update = self.init_last_candles_update(self.db)
        self.last_candles_update_closed = self.init_last_candles_update_closed(self.db)


    def init_history_downloaded(self, db: DataBase) -> Dict:
        hist = {}
        for s in db.selected_symbols:
            hist[s] = {}
            for iv in db.options.window_intervals:
                hist[s][iv] = False
        return hist


    def init_last_candles_update(self, db: DataBase) -> Dict:
        update = {}
        for s in db.selected_symbols:
            update[s] = None
        return update


    def init_last_candles_update_closed(self, db: DataBase) -> Dict:
        closed = {}
        for s in db.selected_symbols:
            closed[s] = False
        return closed
