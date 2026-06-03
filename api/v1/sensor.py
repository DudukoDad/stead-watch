from datetime import datetime
from typing import Dict

from dependencies import get_sqlalchemy_repository
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.sensor_data import SensorDataModel
from schemas.sensor_metadata import SensorModel





router = APIRouter(tags=["sensors"])


# @router.post("/sensor-data/", status_code=status.HTTP_201_CREATED)
# async def add_sensor_data(sensor_data: SensorDataModel):
#     """
#     Endpoint to receive sensor data from IoT devices."""
#     return {
#         "measurement": sensor_data.measurement,
#         "tags": {
#             "device_id": sensor_data.device_id,
#             "location": sensor_data.location,
#             "timestamp": sensor_data.timestamp,
#         },
#         "fields": {
#             "sensor_data": sensor_data.sensor_data,
#         }
#     }

@router.post("/sensor/",  status_code=status.HTTP_201_CREATED)
async def add_sensor(sensor: SensorModel, repo=Depends(get_sqlalchemy_repository)):
    new_sensor = repo.create(
        sensor
    )
    return new_sensor
    

# @router.get("/sensor-data/{device_id}")
# async def get_sensor_data(device_id: str):
#     return {"message": f"Sensor data for device {device_id} retrieved!!!"}


# @router.get("/sensor-data/")
# async def get_sensor_data():
#     return {"message": "Sensor data retrieved!!!"}



