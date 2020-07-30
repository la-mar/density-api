from datetime import datetime
from typing import Optional

from schemas.bases import BaseModel

__all__ = ["CountOut"]


class CountBase(BaseModel):
    """ Base model defining properties shared across schemas """

    space_id: Optional[int]
    timestamp: Optional[datetime]
    count: Optional[int]


class CountOut(CountBase):
    """ Schema defining properties to include in API responses """

    class Config(BaseModel.Config):
        orm_mode = True

    space_id: int
    timestamp: datetime
    count: int
