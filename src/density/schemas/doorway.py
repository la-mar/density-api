from typing import Optional

from pydantic import Field

from schemas.bases import BaseModel, ORMBase

__all__ = ["DoorwayOut", "DoorwayCreateIn", "DoorwayUpdateIn"]


class DoorwayBase(BaseModel):
    """ Base model defining properties shared across schemas """

    name: Optional[str] = Field(None, max_length=100)
    ingress_space_id: Optional[int]
    egress_space_id: Optional[int]


class DoorwayCreateIn(DoorwayBase):
    """ Schema defining properties to available to post requests """

    name: str = Field(..., max_length=100)


class DoorwayUpdateIn(DoorwayBase):
    """ Schema defining properties available to put/patch requests """


class DoorwayOut(ORMBase, DoorwayBase):
    """ Schema defining properties to include in API responses """

    name: str
