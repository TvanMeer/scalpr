# pylint: disable=no-name-in-module

import asyncio
from typing import Any

from pydantic import BaseModel

from ..core.message import UserInput
from ..core.state import SharedState


def format_response(data: BaseModel, formatting: str) -> Any:
    """Helperfunc for user_input_listener."""

    if formatting == "nested_class":
        return data
    if formatting == "dict":
        return data.to_dict()


def query_db(user_input: UserInput, state: SharedState) -> Any:
    """Helperfunc for user_input_listener."""

    formatting = user_input.as_datatype
    if user_input.get_db:
        model = state.db
    elif user_input.timeframe:
        model = state.db.symbols[user_input.symbol].windows[user_input.window].timeframes[user_input.timeframe]
    elif user_input.window:
        model = state.db.symbols[user_input.symbol].windows[user_input.window]
    elif user_input.symbol:
        model = state.db.symbols[user_input.symbol]
    else:
        raise Exception("Error in Bot during user input creation.")
    return format_response(model, formatting)


async def user_input_listener(state: SharedState):
    """Get message from queue, passed in queue from Bot class. Query database and pass response back to the queue."""

    while not state.stop:
        await asyncio.sleep(0.1)
        if state.userinput_queue.not_empty():
            inp = state.userinput_queue.get()
            if inp.shutdown:
                state.stop = True
            else:
                resp = query_db(inp, state.db)
                state.userinput_queue.put(resp)
            state.userinput_queue.task_done()
