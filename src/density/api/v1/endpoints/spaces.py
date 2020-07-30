import logging
from typing import Dict, List

import starlette.status as codes
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from api.helpers import Pagination
from db.models import Space as ORMSpace
from schemas.space import SpaceCreateIn, SpaceOut, SpaceUpdateIn

logger = logging.getLogger(__name__)

router = APIRouter()

ERROR_404: Dict = dict(status_code=codes.HTTP_404_NOT_FOUND, detail="space not found")


@router.post("/", response_model=SpaceOut)
async def create_space(space: SpaceCreateIn):
    """
    Description Here
    """

    return await ORMSpace.create(**space.dict())


@router.get("/", response_model=List[SpaceOut])
async def list_spaces(
    response: ORJSONResponse, pagination: Pagination = Depends(Pagination)
):
    """
    Description Here
    """
    data, headers = await pagination.paginate_links(ORMSpace, serializer=None)

    response = pagination.set_headers(response, headers)

    return data


@router.get("/{id}", response_model=SpaceOut)
async def retrieve_space(id: int):
    """
    Description Here
    """
    space: SpaceOut = await ORMSpace.get(id)
    if not space:
        raise HTTPException(**ERROR_404)

    space = space.to_dict()

    return space


@router.put("/{id}", response_model=SpaceOut, status_code=codes.HTTP_200_OK)
async def update_space_full(body: SpaceUpdateIn, id: int):
    """
    Description Here
    """
    space: ORMSpace = await ORMSpace.get(id)
    if not space:
        raise HTTPException(**ERROR_404)

    await space.update(**body.dict()).apply()
    return space


@router.patch("/{id}", response_model=SpaceOut, status_code=codes.HTTP_200_OK)
async def update_space_partial(body: SpaceUpdateIn, id: int):
    """
    Description Here
    """
    space: ORMSpace = await ORMSpace.get(id)
    if not space:
        raise HTTPException(**ERROR_404)

    await space.update(**body.dict(exclude_unset=True)).apply()
    return space


@router.delete("/{id}", response_model=SpaceOut)
async def delete_space(id: int):
    space: ORMSpace = await ORMSpace.get(id)
    if not space:
        raise HTTPException(**ERROR_404)

    await space.delete()
    return space
