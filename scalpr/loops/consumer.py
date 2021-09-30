import asyncio

from ..core.constants import ContentType
from ..database.database import DataBase
from ..pipeline.candle_pipe import CandlePipe, HistoricalCandlePipe
from .shared_vars import Shared


async def consumer(shared: Shared, q: asyncio.Queue, db: DataBase):
    pipes = {
        ContentType.CANDLE_HISTORY: HistoricalCandlePipe(),
        ContentType.CANDLE_STREAM: CandlePipe(),
        # ...
    }
    while not shared.shutdown:
        msg = await shared.queue.get()
        db = pipes[msg.content_type].process(msg, db)
