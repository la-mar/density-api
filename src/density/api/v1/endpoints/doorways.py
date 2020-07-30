import logging
from typing import Dict, List

import starlette.status as codes
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from api.helpers import Pagination
from db.models import Doorway as ORMDoorway
from schemas.doorway import DoorwayCreateIn, DoorwayOut, DoorwayUpdateIn

logger = logging.getLogger(__name__)

router = APIRouter()

ERROR_404: Dict = dict(status_code=codes.HTTP_404_NOT_FOUND, detail="doorway not found")


@router.post("/", response_model=DoorwayOut)
async def create_doorway(doorway: DoorwayCreateIn):
    """
    Description Here
    """

    return await ORMDoorway.create(**doorway.dict())


@router.get("/", response_model=List[DoorwayOut])
async def list_doorways(
    response: ORJSONResponse, pagination: Pagination = Depends(Pagination)
):
    """
    Description Here
    """
    data, headers = await pagination.paginate_links(ORMDoorway, serializer=None)

    response = pagination.set_headers(response, headers)

    return data


@router.get("/{id}", response_model=DoorwayOut)
async def retrieve_doorway(id: int):
    """
    Description Here
    """
    doorway: DoorwayOut = await ORMDoorway.get(id)
    if not doorway:
        raise HTTPException(**ERROR_404)
    doorway = doorway.to_dict()

    return doorway


@router.put("/{id}", response_model=DoorwayOut, status_code=codes.HTTP_200_OK)
async def update_doorway_full(body: DoorwayUpdateIn, id: int):
    """
    Description Here
    """
    doorway: ORMDoorway = await ORMDoorway.get(id)
    if not doorway:
        raise HTTPException(**ERROR_404)

    await doorway.update(**body.dict()).apply()
    return doorway


@router.patch("/{id}", response_model=DoorwayOut, status_code=codes.HTTP_200_OK)
async def update_doorway_partial(body: DoorwayUpdateIn, id: int):
    """
    Description Here
    """
    doorway: ORMDoorway = await ORMDoorway.get(id)
    if not doorway:
        raise HTTPException(**ERROR_404)

    await doorway.update(**body.dict(exclude_unset=True)).apply()
    return doorway


@router.delete("/{id}", response_model=DoorwayOut)
async def delete_doorway(id: int):
    doorway: ORMDoorway = await ORMDoorway.get(id)
    if not doorway:
        raise HTTPException(**ERROR_404)

    await doorway.delete()
    return doorway
