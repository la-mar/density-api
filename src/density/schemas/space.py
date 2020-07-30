from typing import Optional

from pydantic import Field

from schemas.bases import BaseModel, ORMBase

__all__ = ["SpaceOut", "SpaceCreateIn", "SpaceUpdateIn"]


class SpaceBase(BaseModel):
    """ Base model defining properties shared across schemas """

    name: Optional[str] = Field(None, max_length=100)


class SpaceCreateIn(SpaceBase):
    """ Schema defining properties to available to post requests """

    name: str = Field(..., max_length=100)


class SpaceUpdateIn(SpaceBase):
    """ Schema defining properties available to put/patch requests """


class SpaceOut(ORMBase, SpaceBase):
    """ Schema defining properties to include in API responses """

    name: str
