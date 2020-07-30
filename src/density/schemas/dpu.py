from typing import Optional

from schemas.bases import BaseModel, ORMBase

__all__ = ["DPUOut", "DPUCreateIn", "DPUUpdateIn"]


class DPUBase(BaseModel):
    """ Base model defining properties shared across schemas """

    doorway_id: Optional[int]


class DPUCreateIn(DPUBase):
    """ Schema defining properties to available to post requests """

    id: int


class DPUUpdateIn(DPUBase):
    """ Schema defining properties available to put/patch requests """


class DPUOut(ORMBase, DPUBase):
    """ Schema defining properties to include in API responses """
