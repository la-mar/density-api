from datetime import datetime
from enum import IntEnum
from typing import Optional

from schemas.bases import BaseModel, ORMBase

__all__ = ["ReadingOut", "ReadingCreateIn", "ReadingUpdateIn"]


class SignalEnum(IntEnum):
    IN = 1
    OUT = -1


class ReadingBase(BaseModel):
    """ Base model defining properties shared across schemas """

    dpu_id: Optional[int]
    timestamp: Optional[datetime]
    direction: Optional[SignalEnum]


class ReadingCreateIn(ReadingBase):
    """ Schema defining properties to available to post requests """

    dpu_id: int
    timestamp: datetime
    direction: SignalEnum


class ReadingUpdateIn(ReadingBase):
    """ Schema defining properties available to put/patch requests """


class ReadingOut(ORMBase, ReadingBase):
    """ Schema defining properties to include in API responses """

    id: Optional[int]
    timestamp: datetime
    direction: SignalEnum
