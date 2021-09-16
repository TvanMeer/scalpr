# pylint: disable=no-name-in-module

from collections.abc import Iterable
from typing import Callable, Optional, Set

from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError
from pydantic.types import DirectoryPath

from .core.constants import Interval, Mode, Stream


class Options(BaseModel):
    """All options for scalpr.
    Required by Bot object at initialization.
    """

    key:              str                     = " "
    secret:           str                     = " "
    mode:             Mode                    = Mode.TEST
    datadir:          Optional[DirectoryPath] = None
    base_assets:      Set[str]                = {"BTC", "HOT"}
    quote_assets:     Set[str]                = {"USDT"}
    window_intervals: Set[Interval]           = {Interval.SECOND_2, Interval.MINUTE_1}
    window_length:    int                     = 200
    streams:          Optional[Set[Stream]]   = {Stream.CANDLE, Stream.DEPTH5, Stream.MINITICKER}
    #features:         Optional[Set[Callable]] = None



    @validator("key", "secret")
    @classmethod
    def _check_credentials(cls, v):
        if not v == " " and not len(v) == 64:
            raise ValidationError("Both key and secret should be of length 64.")
        if not v == " " and not v.isalnum():
            raise ValidationError("Both key and secret should be alphanumeric.")
        return v



    @validator("base_assets", "quote_assets", pre=True)
    @classmethod
    def _check_asset_names(cls, v):
        def check_str(s):
            if not len(s) in range(3, 7):
                raise ValidationError("Asset names should be between 3 and 6 characters long.")
            if not s.isalnum():
                raise ValidationError("Asset names should be alphanumeric, like `BTC` or `USDC`.")

        if isinstance(v, str):
            check_str(v)
            return {v.lower()}
        elif isinstance(v, Iterable):
            [check_str(s) for s in v]
            lower = set(map(lambda s: s.lower(), v))
            return lower
        else:
            raise ValidationError("Asset names should be strings.")



    @validator("window_intervals", pre=True)
    @classmethod
    def _make_window_intervals(cls, v):

        def iv(val):
            val = val.lower()
            if val in Interval.list():
                return Interval(val)
            else:
                raise ValidationError("Invalid window intervals.")

        if isinstance(v, str):
            return {iv(v)}
        elif isinstance(v, Iterable):
            itvs = set()
            [itvs.add(iv(s)) for s in v]
            return itvs
        else:
            raise ValidationError("Invalid window intervals: should be strings.")



    @validator("window_length", pre=True)
    @classmethod
    def _check_window_length(cls, v):
        if v == "*":
            return 0
        elif isinstance(v, int) and v >= 0:
            return v
        else:
            raise ValidationError("Invalid window length.")



    @validator("streams", pre=True)
    @classmethod
    def _make_streams(cls, v):

        def stream(val):
            val = val.upper()
            if val in Stream.list():
                return Stream(val)
            else:
                raise ValidationError("Invalid streams.")

        if isinstance(v, str):
            return {stream(v)}
        elif isinstance(v, Iterable):
            strms = set()
            [strms.add(stream(s)) for s in v]
            return strms
        else:
            raise ValidationError("Invalid streams: should be strings.")

