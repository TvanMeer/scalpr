from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from pydantic import BaseModel, ValidationError

from ..core.constants import ContentType, InTimeFrame
from ..core.message import Message
from ..core.state import SharedState
from ..database.timeframe import TimeFrame
from ..database.window import Window


class Pipe(ABC):
    """Handles parsing and insertion of a Message object into the database."""

    def process(self, message: Message, state: SharedState) -> SharedState:
        """Template method that sends the message through the pipeline."""

        message.close_time = self.get_close_time(message)   # Child function call
        message.parsed = self.parse(message)                # Child function call
        message.corrupt = self.validate(message, state)     # Child function call
        state = self.update_state(message, state)           # Child function call
        state = self.insert_in_db(message, state)           # Executes all super functions
        return state


    def insert_in_db(self, message: Message, state: SharedState) -> SharedState:
        if message.interval:
            return self.insert_in_window(message, state)
        else:
            return self.insert_in_all_windows(message, state)


    def insert_in_all_windows(self, message: Message, state: SharedState) -> SharedState:
        for interval in state.db.options.window_intervals:
            message.interval = interval
            return self.insert_in_window(message, state)


    def insert_in_window(self, message: Message, state: SharedState) -> SharedState:
        window = state.db.symbols[message.symbol].windows[message.interval]
        updated_window = self.insert_in_timeframe(message, state, window)
        state.db.symbols[message.symbol].windows[message.interval] = updated_window
        return state


    def insert_in_timeframe(self, message: Message, state: SharedState, window: Window) -> Window:
        in_timeframe = self.which_timeframe(message, state, window)
        match in_timeframe:
            case InTimeFrame.IGNORE:
                return window
            case InTimeFrame.FIRST:
                window = self.create_first_timeframe(message, window)
                return self.first_in_timeframe(message, window, in_timeframe)
            case InTimeFrame.PREVIOUS:
                return self.update_timeframe(message, window, in_timeframe)
            case InTimeFrame.CURRENT:
                return self.update_timeframe(message, window, in_timeframe)
            case InTimeFrame.NEXT:
                window = self.create_next_timeframe(window)
                return self.first_in_timeframe(message, window, in_timeframe)
            case InTimeFrame.OTHER:
                e = """Cannot keep up with data processing. 
                Perhaps you selected too many streams."""
                raise Exception(e)


    def which_timeframe(self, message: Message, state: SharedState, window: Window) -> InTimeFrame:
        """Determines in which timeframe message.payload should be inserted."""

        if not window.timeframes:
            match message.content_type:
                case ContentType.CANDLE_HISTORY:
                    return InTimeFrame.FIRST
                case _:
                    return InTimeFrame.IGNORE
            
        if not state.history_downloaded:
            return InTimeFrame.IGNORE

        tf = window.timeframes[-1]
        milli = timedelta(milliseconds=1)
        delta = tf.close_time - tf.open_time + milli

        if message.close_time > tf.close_time + delta:
            raise Exception("Timing error in timeframe creation.")
        if message.close_time > tf.close_time:
            return InTimeFrame.NEXT
        if message.close_time > tf.open_time:
            return InTimeFrame.CURRENT
        if message.close_time > tf.open_time - delta:
            return InTimeFrame.PREVIOUS
        return InTimeFrame.OTHER


    def create_timeframe(self, open_time: datetime, close_time: datetime, window: Window) -> Window:
        """Creates a new TimeFrame instance. Appends the new instance to the deque of timeframes in the window."""

        try:
            new_tf = TimeFrame(
                open_time=open_time,
                close_time=close_time
            )
            return window.timeframes.append(new_tf)
        except ValidationError as e:
            print(e)


    def create_first_timeframe(self, message: Message, window: Window) -> Window:
        """Creates and adds the very first timeframe in an empty window."""

        match message.content_type:
            case ContentType.CANDLE_HISTORY:
                open_time = self.to_datetime(message.payload[0])
                close_time = self.to_datetime(message.payload[6])
                return self.create_timeframe(open_time, close_time, window)
            case _:
                raise Exception(f"Cannot create first timeframe with {message.content_type.value}.")


    def create_next_timeframe(self, window: Window) -> Window:
        """Creates and adds the next new empty timeframe in the deque of window.timeframes."""

        last_tf = window[-1]
        last_open = last_tf.open_time
        last_close = last_tf.close_time
        milli = timedelta(milliseconds=1)
        delta = last_close - last_open + milli
        return self.create_timeframe(last_open + delta, last_close + delta, window)


    @abstractmethod
    def get_close_time(self, message: Message) -> datetime:
        """Returns the close time or event time of content in message."""

    @abstractmethod
    def parse(self, message: Message) -> BaseModel:
        """Parses message.payload and returns a pydantic BaseModel."""

    @abstractmethod
    def validate(self, message: Message, state: SharedState) -> bool:
        """Returns True if the data in message.payload is corrupt."""

    @abstractmethod
    def update_state(self, message: Message, state: SharedState) -> SharedState:
        """Updates variables in state, excluding state.db"""

    @abstractmethod
    def first_in_timeframe(self, message: Message, window: Window, position: InTimeFrame) -> Window:
        """Inserts message.payload in the first timeframe of the window, or in
        the next empty timeframe that has just been created.
        """

    @abstractmethod
    def update_timeframe(self, message: Message, window: Window, position: InTimeFrame) -> Window:
        """Updates the current or previous timeframe with message.payload."""


    # Helper functions ---------------------------------------------------------


    def to_datetime(self, time: str) -> datetime:
        """Converts a Binance timestamp to a datetime object."""

        return datetime.fromtimestamp(int(time)/1000)


    def round_time(self, close_time: datetime):
        """Rounds close_time to the closest second. Then substracts 1ms.
        Used to calculate Interval.SECONDS_2 candle close time based on event time.
        """
      
        rounded = close_time - timedelta(microseconds=close_time.microsecond)
        close_time = rounded - timedelta(milliseconds=1)
        return close_time


    

        