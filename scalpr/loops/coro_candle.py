import asyncio
from typing import Dict

from binance import AsyncClient, BinanceSocketManager

from ..core.constants import ContentType
from ..pipeline.pipe import Message, Pipe
from ..core.state import SharedState


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



def fake_candle(i: int, symbol: str) -> Dict:
    """Helper func for mock candle producer."""

    t = 1632800640000
    T = 1632800699999
    t += i * 60000
    T += i * 60000

    return {
        "e": "kline",
        "E": t + 10000,
        "s": "BTCUSDT",
        "k": {
            "t": t,
            "T": T,
            "s": "BTCUSDT",
            "i": "1m",
            "f": i * 1000000000,
            "L": i * 1000000100,
            "o": str(i * 10000) + ".00000000",
            "c": str(i * 11000) + ".00000000",
            "h": str(i * 11500) + ".00000000",
            "l": str(i * 9500)  + ".00000000",
            "v": str(i * 0.25)  + "000000",
            "n": i * 10,
            "x": False,
            "q": str(i * 10000) + ".00000000",
            "V": str(i * 0.1)   + "0000000",
            "Q": str(i * 5000)  + ".00000000",
            "B": "0"
        }
    }


async def mock_candle_producer(state: SharedState, symbol: str):
    """Produces a fake candle, every two seconds."""

    i = 1
    while not state.stop:
        asyncio.sleep(2)
        raw_candle = fake_candle(i, symbol)
        message = Message(
                time         =Pipe.to_datetime(time=raw_candle["k"]["T"]),
                symbol       =symbol,
                content_type =ContentType.CANDLE_STREAM,
                payload      =raw_candle
            )
        await state.queue.put(message)
        next_i = i + 1 if i <= 10 else 1
        i = next_i
