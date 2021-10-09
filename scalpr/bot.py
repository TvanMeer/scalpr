from queue import Queue
from threading import Thread
from typing import Any

from .core.constants import Interval
from .core.manager import Manager
from .core.message import UserInput
from .options import Options


class Bot:
    def __init__(self, options: Options):
        self.options = options
        self._queue = Queue()
        self._manager = Thread(target=self._create_manager, args=(self.options, self._queue))
        self._manager.start()


    def _create_manager(self, options: Options, queue: Queue):
        m = Manager()
        m.start(options, queue)


    def _query(self, inp: UserInput) -> Any:
        self._queue.put(inp)
        self._queue.join()
        resp = self._queue.get()
        return resp
    

    # Public interface
    def get_database(self, as_datatype="nested_class") -> Any:
        inp = UserInput()
        inp.get_db = True
        inp.as_datatype = as_datatype
        return self._query(inp)


    def get_symbol(self, symbol: str, as_datatype="nested_class") -> Any:
        inp = UserInput()
        inp.symbol = symbol
        inp.as_datatype = as_datatype
        return self._query(inp)


    def get_window(self, symbol: str, interval: str, as_datatype="nested_class") -> Any:
        inp = UserInput()
        inp.symbol = symbol
        inp.window = Interval(interval)
        inp.as_datatype = as_datatype
        return self._query(inp)


    def get_timeframe(self, symbol: str, interval: str, index: int, as_datatype="nested_class") -> Any:
        inp = UserInput()
        inp.symbol = symbol
        inp.window = Interval(interval)
        inp.timeframe = index
        inp.as_datatype = as_datatype
        return self._query(inp)


    def stop(self):
        print("Shutting down Scalpr...")
        inp = UserInput()
        inp.shutdown = True
        _ = self._query(inp)
        self._manager.join()
        print("Scalpr shut down gracefully.")
        
