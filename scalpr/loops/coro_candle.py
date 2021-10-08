import asyncio

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import ContentType
from ..pipeline.pipe import Message, Pipe
from .state import SharedState


async def candle_producer(state: SharedState, symbol: str, manager: BinanceSocketManager):
    """Stream candle data for one specific symbol."""

    socket = manager.kline_socket(symbol=symbol)
    async with socket as candle_socket:
        while not state.stop:
            raw_candle = await candle_socket.recv()
            message = Message(
                time         =Pipe.to_datetime(time=raw_candle["k"]["T"]),
                symbol       =symbol,
                content_type =ContentType.CANDLE_STREAM,
                payload      =raw_candle
            )
            await state.queue.put(message)



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

   
async def historical_candle_producer(state: SharedState, client: AsyncClient):
    """Download candle history for all selected symbols and window intervals."""

    window_length = state.db.options.window_length
    intervals = state.db.options.window_intervals
    symbols = state.db.selected_symbols

    for s in symbols:
        for iv in intervals:
            time_string = to_timestring(iv.value, window_length)
            candles = await client.get_historical_klines(s, iv.value, time_string, limit=window_length)
            if len(candles) < window_length:
                raise Exception(f"Binance API did not return enough candles for {s} {iv}. Only {len(candles)} instead of {window_length}.")
            for c in candles:
                message = Message(
                    time         =Pipe.to_datetime(time=c[6]),
                    symbol       =s,
                    content_type =ContentType.CANDLE_HISTORY,
                    payload      =c,
                    interval     =iv
                )
                await state.queue.put(message)
            if state.stop: break
            await asyncio.sleep(4)
            if state.stop: break


async def mock_candle_producer(state: SharedState, symbol: str):
    pass #TODO
