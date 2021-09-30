from binance import AsyncClient, BinanceSocketManager

from ..core.constants import ContentType
from ..pipeline.pipe import Message, Pipe
from .shared_vars import Shared


async def candle_producer(symbol: str, shared: Shared, client: AsyncClient, manager: BinanceSocketManager):
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

