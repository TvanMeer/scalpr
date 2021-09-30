from typing import Set

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import ContentType, Interval
from ..pipeline.pipe import Message, Pipe
from .shared_vars import Shared


async def candle_producer(symbol: str, shared: Shared, manager: BinanceSocketManager):
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


async def historical_candle_producer(symbol: str, shared: Shared, intervals: Set[Interval], windowsize: int, client: AsyncClient):

    def to_timestring(interval: str, windowsize: int) -> str:
        amount = int(interval[:-1]) * windowsize
        time_frame = interval[-1]
        time_frames = {
            "m": f"{amount} minutes ago UTC",
            "h": f"{amount} hours ago UTC",
            "d": f"{amount} days ago UTC",
            "w": f"{amount} weeks ago UTC"
        }
        return time_frames[time_frame]

    for iv in intervals:
        time_string = to_timestring(iv.value, windowsize)
        candles= await client.get_historical_klines(symbol, iv.value, time_string,limit=windowsize)
        for c in candles:
            message = Message(
                time         =Pipe.to_datetime(time=c[6]),
                symbol       =symbol,
                content_type =ContentType.CANDLE_HISTORY,
                payload      =c,
                interval     =iv
            )
            await shared.queue.put(message)
        if shared.shutdown: break
