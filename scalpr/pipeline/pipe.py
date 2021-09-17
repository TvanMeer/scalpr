# pylint: disable=no-name-in-module

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from pydantic.main import BaseModel
from scalpr.database.database import DataBase
from scalpr.database.window import Window

from ..core.constants import ContentType, InTimeFrame


class Pipe(ABC):
    """Handles insertion of content in the database."""
      

    def process(
        self, 
        contenttype: ContentType, 
        payload:     Any, 
        meta:        dict, 
        db:          DataBase
    ) -> DataBase:
        """Calls process_window() for the windows that should be updated."""

        symbol   = meta["symbol"]
        interval = meta["interval"]

        def one_window(self):
            db.symbols[symbol].windows[interval] = self.process_window(
                contenttype, payload, db.symbols[symbol].windows[interval]
            )

        def all_windows(self):
            for iv, w in db.symbols[symbol].windows.items():
                db.symbols[symbol].windows[iv] = self.process_window(contenttype, payload, w)

        apply_on_windows = {
            ContentType.CANDLE_HISTORY: one_window,
            ContentType.CANDLE_STREAM:  all_windows,
        }
        apply_on_windows[contenttype]()
        return db


    def process_window(
        self, 
        contenttype: ContentType, 
        payload:     Any, 
        window:      Window
    ) -> Window:
        """Updates a single window."""

        if not window._history_downloaded and contenttype == ContentType.CANDLE_STREAM:
            return window

        tf = {
            InTimeFrame.FIRST:    self.insert_in_first_timeframe,
            InTimeFrame.PREVIOUS: self.insert_in_previous_timeframe,
            InTimeFrame.CURRENT:  self.insert_in_current_timeframe,
            InTimeFrame.NEXT:     self.insert_in_next_timeframe,
            InTimeFrame.OTHER:    self.data_leakage_error,
        }

        in_tf = self.which_timeframe(payload, window)
        return tf[in_tf](payload, window)



    @abstractmethod
    def parse(self, payload: Any) -> BaseModel:
        raise NotImplementedError
        
    @abstractmethod
    def which_timeframe(self, payload: Any, window: Window) -> InTimeFrame:
        raise NotImplementedError

    @abstractmethod
    def insert_in_first_timeframe(self, payload: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_previous_timeframe(self, payload: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_current_timeframe(self, payload: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_next_timeframe(self, payload: Any, window: Window) -> Window:
        raise NotImplementedError



    # Helper funcs ------------------------------------------------------------

    def data_leakage_error(self, *args):
        e = """Data leakage: bbot cannot process the data fast enough. 
        Reduce the number of data sources or try to increase the performance
        of your feature calculation functions.
        """
        raise Exception(e)


    def round_time(self, close_time: datetime):
        """Rounds time to closest possible 2-second close time -1ms.
        Used to get 2 second candle close time based on event time.
        """
      
        rounded = close_time - timedelta(microseconds=close_time.microsecond)
        close_time = rounded - timedelta(milliseconds=1)
        return close_time
