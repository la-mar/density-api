from fastapi import APIRouter

from api.v1.endpoints.counts import router as counts_router
from api.v1.endpoints.doorways import router as doorway_router
from api.v1.endpoints.dpus import router as dpu_router
from api.v1.endpoints.health import router as health_router
from api.v1.endpoints.readings import router as readings_router
from api.v1.endpoints.spaces import router as space_router

__all__ = ["api_router"]

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(space_router, prefix="/spaces", tags=["Spaces"])
api_router.include_router(doorway_router, prefix="/doorways", tags=["Doorways"])
api_router.include_router(
    dpu_router, prefix="/dpus", tags=["Density Processing Units (DPUs)"]
)
api_router.include_router(readings_router, prefix="/readings", tags=["Readings"])
api_router.include_router(counts_router, prefix="/counts", tags=["Space Counts"])
