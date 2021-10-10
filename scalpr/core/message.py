# pylint: disable=no-name-in-module

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .constants import ContentType, Interval


@dataclass
class UserInput:
    """A query or shutdown request passed from the main thread to the
    user input coroutine in the secondary thread, through the user input
    queue.
    """

    shutdown:    bool     = False
    get_db:      bool     = False
    symbol:      str      = None
    window:      Interval = None
    timeframe:   int      = None
    as_datatype: str      = "nested_class"

@dataclass
class Message:
    """A message from a websocket or API request, passed in
    an asyncio queue and consumed by the consumer coroutine. Then
    passed from the consumer through the corresponding content types
    pipeline.
    """

    time:         datetime
    symbol:       str
    content_type: ContentType
    payload:      Union[Dict, List]
    interval:     Optional[Interval]  = None
    parsed:       Optional[BaseModel] = None
