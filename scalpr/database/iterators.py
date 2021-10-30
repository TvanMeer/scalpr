from collections.abc import Iterable, Iterator

from .data import DataBase, Window


class WindowIterator(Iterator):
    """Iterator that iterates over all windows of a given symbol."""

    _windows_left: set[str] = None

    def __init__(self, symbol: str, db: DataBase):
        self.symbol = symbol
        self.db = db
        self._windows_left = set(db.symbols[symbol].windows.keys())

    def __next__(self) -> Window:
        try:
            window_str = self._windows_left.pop()
        except KeyError as windows_done:
            raise StopIteration() from windows_done
        return self.db.symbols[self.symbol].windows[window_str]



class WindowIterable(Iterable):
    """Iterable to initialize before iterating over all windows of a given symbol.
    
    Example:

    for window in WindowIterable(symbol, db):
        ...
        
    """

    def __init__(self, symbol: str, db: DataBase):
        self.symbol = symbol
        self.db = db

    def __iter__(self) -> WindowIterator:
        return WindowIterator(self.symbol, self.db)
