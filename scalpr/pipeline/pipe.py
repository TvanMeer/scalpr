# pylint: disable=no-name-in-module

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError

from ..core.constants import ContentType, Interval, InTimeFrame
from ..database.database import DataBase
from ..database.timeframe import TimeFrame
from ..database.window import Window


@dataclass
class Message:
    """A message from the consumer."""

    time:         datetime
    symbol:       str
    content_type: ContentType
    payload:      Union[Dict, List]
    interval:     Optional[Interval]  = None
    parsed:       Optional[BaseModel] = None

class Pipe(ABC):
    """Handles insertion of content in the database."""

    def process(self, message: Message, db: DataBase) -> DataBase:
        """Updates one or all windows for a symbol."""

        apply_on_windows = {
            ContentType.CANDLE_HISTORY: self.one_window,
            ContentType.CANDLE_STREAM:  self.all_windows,
            #...
        }
        db = apply_on_windows[message.content_type](message, db)
        return db


    def one_window(self, message: Message, db: DataBase) -> DataBase:
        """Pipes message to a single window for a symbol, by calling process_window."""

        db.symbols[message.symbol].windows[message.interval] = self.process_window(
            message, db.symbols[message.symbol].windows[message.interval]
        )
        return db


    def all_windows(self, message: Message, db: DataBase) -> DataBase:
        """Pipes message to all windows for a symbol, by calling process_window on all windows."""

        for iv, w in db.symbols[message.symbol].windows.items():
            db.symbols[message.symbol].windows[iv] = self.process_window(message, w)
        return db



    def process_window(self, message: Message, window: Window) -> Window:
        """Updates a single window."""

        tf = {
            InTimeFrame.FIRST:    self.insert_in_first_timeframe,
            InTimeFrame.PREVIOUS: self.insert_in_previous_timeframe,
            InTimeFrame.CURRENT:  self.insert_in_current_timeframe,
            InTimeFrame.NEXT:     self.insert_in_next_timeframe,
        }

        position = self.which_timeframe(message, window)
        if position == InTimeFrame.IGNORE:
            pass
        if position == InTimeFrame.OTHER:
            self.data_leakage_error()

        window = self.before(message, window)
        message.parsed = self.parse(message.payload)
        window.timeframes[-1].corrupt = self.validate(message, window)
        window = tf[position](message, window)
        return window


    def which_timeframe(self, message: Message, window: Window) -> InTimeFrame:
        """Determines timeframe position where message payload should be inserted."""

        if not window.timeframes:
            if message.content_type == ContentType.CANDLE_HISTORY:
                return InTimeFrame.FIRST
            else:
                return InTimeFrame.IGNORE
        if not window._history_downloaded:
            return InTimeFrame.IGNORE

        tf = window.timeframes[-1]
        milli = timedelta(milliseconds=1)
        delta = tf.close_time - tf.open_time + milli

        if message.time > tf.close_time + delta:
            raise Exception("Error in timeframe creation.")
        if message.time > tf.close_time:
            return InTimeFrame.NEXT
        if message.time > tf.open_time:
            return InTimeFrame.CURRENT
        if message.time > tf.open_time - delta:
            return InTimeFrame.PREVIOUS
        return InTimeFrame.OTHER


    @abstractmethod
    def before(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def parse(self, payload: Union[Dict, List]) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def validate(self, message: Message, window: Window) -> bool:
        raise NotImplementedError

    def insert_in_first_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError # Overwritten in HistoricalCandlePipe

    @abstractmethod
    def insert_in_previous_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_current_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError

    @abstractmethod
    def insert_in_next_timeframe(self, message: Message, window: Window) -> Window:
        raise NotImplementedError



    # Helper funcs ------------------------------------------------------------

    def data_leakage_error(self):
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


    def to_datetime(self, time: str) -> datetime:
        """Converts a Binance timestamp to a datetime object."""

        return datetime.fromtimestamp(int(time)/1000)


    def add_empty_timeframe(self, open_time: datetime, close_time: datetime, window: Window) -> Window:
        """Adds an empty timeframe to window.timeframes"""

        try:
            tf = TimeFrame(
                open_time  = open_time,
                close_time = close_time,
            )
            window.timeframes.append(tf)
            return window
        except ValidationError as e:
            raise Exception(e)


    def add_next_empty_timeframe(self, window: Window) -> Window:
        """Adds the next new empty timeframe to window.timeframes."""

        prev_ot = window.timeframes[-1].open_time
        prev_ct = window.timeframes[-1].close_time
        milli = timedelta(milliseconds=1)
        delta = prev_ct - prev_ot + milli
        open_time = prev_ot + delta
        close_time = prev_ct + delta
        window = self.add_empty_timeframe(open_time, close_time, window)
        return window
