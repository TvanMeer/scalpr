
import asyncio

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import ContentType
from ..database.database import DataBase
from ..pipeline.pipe import Message, Pipe
from .shared_vars import Shared


async def candle_producer(symbol: str, shared: Shared, manager: BinanceSocketManager):
    """Spawned one for every selected symbol."""

    socket = manager.kline_socket(symbol=symbol)
    async with socket as candle_socket:
        while not shared.shutdown:
            candle = await candle_socket.recv()
            message = Message(
                time         =Pipe.to_datetime(time=candle["k"]["T"]),
                symbol       =symbol,
                content_type =ContentType.CANDLE_STREAM,
                payload      =candle
            )
            await shared.queue.put(message)



def to_timestring(interval: str, window_length: int) -> str:
    """Helper func for downloading history."""

    amount = int(interval[:-1]) * window_length
    time_frame = interval[-1]
    time_frames = {
        "m": f"{amount} minutes ago UTC",
        "h": f"{amount} hours ago UTC",
        "d": f"{amount} days ago UTC",
        "w": f"{amount} weeks ago UTC"
    }
    return time_frames[time_frame]



async def historical_candle_producer(shared: Shared, client: AsyncClient, db: DataBase):
    """Spawned one only for all selected symbols."""

    window_length = db.options.window_length
    intervals = db.options.window_intervals
    symbols = db.selected_symbols

    for s in symbols:
        for iv in intervals:
            time_string = to_timestring(iv.value, window_length)
            candles= await client.get_historical_klines(s, iv.value, time_string, limit=window_length)
            for c in candles:
                message = Message(
                    time         =Pipe.to_datetime(time=c[6]),
                    symbol       =s,
                    content_type =ContentType.CANDLE_HISTORY,
                    payload      =c,
                    interval     =iv
                )
                await shared.queue.put(message)
            db.symbols[s].windows[iv]._history_downloaded = True
            await asyncio.sleep(4)
            if shared.shutdown: break
