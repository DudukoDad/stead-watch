from fastapi import APIRouter
from api.v1 import sensor

router = APIRouter(prefix="/v1")
router.include_router(sensor.router, prefix="/sensors", tags=["sensors"])