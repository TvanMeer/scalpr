# pylint: disable=no-name-in-module

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from pydantic.main import BaseModel
from scalpr.database.database import DataBase
from scalpr.database.window import Window

from ..core.constants import ContentType, InTimeFrame
from ..database.timeframe import TimeFrame


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
        interval = meta["interval"] if "interval" in meta.keys() else None

        def one_window(self):
            db.symbols[symbol].windows[interval] = self._process_window(
                payload, db.symbols[symbol].windows[interval]
            )

        def all_windows(self):
            for iv, w in db.symbols[symbol].windows.items():
                db.symbols[symbol].windows[iv] = self._process_window(payload, w)

        apply_on_windows = {
            ContentType.CANDLE_HISTORY: one_window,
            ContentType.CANDLE_STREAM:  all_windows,
        }
        apply_on_windows[contenttype]()
        return db


    def _process_window(
        self,
        payload:     Any, 
        window:      Window
    ) -> Window:
        """Updates a single window."""


        tf = {
            InTimeFrame.FIRST:    self.insert_in_first_timeframe,
            InTimeFrame.PREVIOUS: self.insert_in_previous_timeframe,
            InTimeFrame.CURRENT:  self.insert_in_current_timeframe,
            InTimeFrame.NEXT:     self.insert_in_next_timeframe,
            InTimeFrame.OTHER:    self.data_leakage_error,
            InTimeFrame.IGNORE:   self.ignore
        }

        in_tf = self.which_timeframe(payload, window)
        parsed = self.parse(payload)
        updated_window = tf[in_tf](parsed, window)
        return updated_window



    @abstractmethod
    def which_timeframe(self, payload: Any, window: Window) -> InTimeFrame:
        raise NotImplementedError

    @abstractmethod
    def parse(self, payload: Any) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def insert_in_first_timeframe(self, parsed: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_previous_timeframe(self, parsed: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_current_timeframe(self, parsed: Any, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_next_timeframe(self, parsed: Any, window: Window) -> Window:
        raise NotImplementedError



    # Helper funcs ------------------------------------------------------------

    def data_leakage_error(self, *args):
        e = """Data leakage: bbot cannot process the data fast enough. 
        Reduce the number of data sources or try to increase the performance
        of your feature calculation functions.
        """
        raise Exception(e)

    def ignore(self, *args):
        """Ignore payload."""

        pass


    def round_time(self, close_time: datetime):
        """Rounds time to closest possible 2-second close time -1ms.
        Used to get 2 second candle close time based on event time.
        """
      
        rounded = close_time - timedelta(microseconds=close_time.microsecond)
        close_time = rounded - timedelta(milliseconds=1)
        return close_time


    def add_new_empty_timeframe(self, window: Window) -> Window:
        """Adds a new empty timeframe to window.timeframes."""

        prev_ot = window.timeframes[-1].open_time
        prev_ct = window.timeframes[-1].close_time
        milli = timedelta(milliseconds=1)
        delta = prev_ct - prev_ot + milli
        tf = TimeFrame(
            open_time  = prev_ot + delta,
            close_time = prev_ct + delta
        )
        window.timeframes.append(tf)
        return window
