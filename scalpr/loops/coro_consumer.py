from ..core.constants import ContentType
from ..pipeline.candle_pipe import CandlePipe, HistoricalCandlePipe
from ..core.state import SharedState


async def consumer(state: SharedState):
    """Takes all messages from the queue and sends these trough the corresponding pipelines."""

    pipes = {
        ContentType.CANDLE_HISTORY: HistoricalCandlePipe(),
        ContentType.CANDLE_STREAM: CandlePipe(),
        # ...
    }
    while not state.stop:
        msg = await state.queue.get()
        state.db = pipes[msg.content_type].process(msg, state.db)
