import functools
import logging
from typing import Dict, List

import starlette.status as codes
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import ORJSONResponse

from api.helpers import Pagination
from db.models import Reading as ORMReading
from schemas.reading import ReadingCreateIn, ReadingOut

logger = logging.getLogger(__name__)

router = APIRouter()

ERROR_404: Dict = dict(status_code=codes.HTTP_404_NOT_FOUND, detail="reading not found")


pagination_with_defaults = functools.partial(Pagination, sort=Query("timestamp"))


@router.post("/", response_model=ReadingOut)
async def create_reading(reading: ReadingCreateIn):
    """
    Create a new reading
    """

    return await ORMReading.create(**reading.dict())


@router.get("/", response_model=List[ReadingOut])
async def list_readings(
    response: ORJSONResponse,
    pagination: Pagination = Depends(pagination_with_defaults),
):
    """
    Get a list of readings
    """

    pagination.sort = pagination.sort or "timestamp"
    data, headers = await pagination.paginate_links(ORMReading, serializer=None)

    response = pagination.set_headers(response, headers)

    return data


@router.get("/{id}", response_model=ReadingOut)
async def retrieve_reading(id: int):
    """
    Get a reading using the reading identifier
    """
    reading: ReadingOut = await ORMReading.query.where(
        ORMReading.id == id
    ).gino.one_or_none()

    if not reading:
        raise HTTPException(**ERROR_404)

    reading = reading.to_dict()

    return reading
