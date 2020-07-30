import logging
from typing import Dict, List

import starlette.status as codes
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from api.helpers import Pagination
from db.models import SpaceCount
from schemas.count import CountOut

logger = logging.getLogger(__name__)

router = APIRouter()

ERROR_404: Dict = dict(status_code=codes.HTTP_404_NOT_FOUND, detail="count not found")


@router.get("/", response_model=List[CountOut])
async def list_counts(
    response: ORJSONResponse, pagination: Pagination = Depends(Pagination)
):
    """
    Get people counts by space over time
    """
    data, headers = await pagination.paginate_links(SpaceCount, serializer=None)

    response = pagination.set_headers(response, headers)

    return data


@router.get("/{space_id}", response_model=List[CountOut])
async def list_counts_by_space(space_id: int):
    """
    Get a list of historical people counts for a given space
    """
    counts: List[CountOut] = await SpaceCount.query.where(
        SpaceCount.space_id == space_id
    ).gino.all()

    if not counts:
        raise HTTPException(**ERROR_404)

    return counts


@router.get("/{space_id}/current", response_model=CountOut)
async def current_space_count(space_id: int):
    """
    Get the current people count for a space
    """
    counts: CountOut = await SpaceCount.query.where(
        SpaceCount.space_id == space_id
    ).order_by(SpaceCount.timestamp.desc()).gino.first()

    if not counts:
        raise HTTPException(**ERROR_404)

    return counts
