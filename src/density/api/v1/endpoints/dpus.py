import logging
from typing import Dict, List

import starlette.status as codes
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from api.helpers import Pagination
from db.models import DPU as ORMDPU
from schemas.dpu import DPUCreateIn, DPUOut, DPUUpdateIn

logger = logging.getLogger(__name__)

router = APIRouter()

ERROR_404: Dict = dict(status_code=codes.HTTP_404_NOT_FOUND, detail="dpu not found")


@router.post("/", response_model=DPUOut)
async def create_dpu(dpu: DPUCreateIn):
    """
    Description Here
    """

    return await ORMDPU.create(**dpu.dict())


@router.get("/", response_model=List[DPUOut])
async def list_dpus(
    response: ORJSONResponse, pagination: Pagination = Depends(Pagination)
):
    """
    Description Here
    """
    data, headers = await pagination.paginate_links(ORMDPU, serializer=None)

    response = pagination.set_headers(response, headers)

    return data


@router.get("/{id}", response_model=DPUOut)
async def retrieve_dpu(id: int):
    """
    Description Here
    """
    dpu: DPUOut = await ORMDPU.get(id)
    if not dpu:
        raise HTTPException(**ERROR_404)

    dpu = dpu.to_dict()

    return dpu


@router.put("/{id}", response_model=DPUOut, status_code=codes.HTTP_200_OK)
async def update_dpu_full(body: DPUUpdateIn, id: int):
    """
    Description Here
    """
    dpu: ORMDPU = await ORMDPU.get(id)
    if not dpu:
        raise HTTPException(**ERROR_404)

    await dpu.update(**body.dict()).apply()
    return dpu


@router.patch("/{id}", response_model=DPUOut, status_code=codes.HTTP_200_OK)
async def update_dpu_partial(body: DPUUpdateIn, id: int):
    """
    Description Here
    """
    dpu: ORMDPU = await ORMDPU.get(id)
    if not dpu:
        raise HTTPException(
            status_code=codes.HTTP_404_NOT_FOUND, detail="dpu not found"
        )

    await dpu.update(**body.dict(exclude_unset=True)).apply()
    return dpu


@router.delete("/{id}", response_model=DPUOut)
async def delete_dpu(id: int):
    dpu: ORMDPU = await ORMDPU.get(id)
    if not dpu:
        raise HTTPException(
            status_code=codes.HTTP_404_NOT_FOUND, detail="dpu not found"
        )

    await dpu.delete()
    return dpu
