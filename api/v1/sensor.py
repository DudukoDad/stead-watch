from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from models.sensor_data import SensorModel


class SensorDataResponse(BaseModel):
    sensor_id: str
    location: str
    timestamp: datetime
    data: Dict[str, float]


router = APIRouter(tags=["sensors"])


@router.post("/sensor-data/", response_model=SensorDataResponse, status_code=status.HTTP_201_CREATED)
async def add_sensor_data(sensor_data: SensorModel):
    """
    Endpoint to receive sensor data from IoT devices."""
    return {
        "sensor_id": sensor_data.device_id,
        "location": sensor_data.location,
        "timestamp": sensor_data.timestamp,
        "data": {
            "sensor_data": sensor_data.sensor_data,
        }
    }




@router.get("/sensor-data/")
async def get_sensor_data():
    return {"message": "Sensor data retrieved!!!"}
