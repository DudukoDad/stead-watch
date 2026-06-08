from datetime import datetime
from typing import Dict

from dependencies import get_sqlalchemy_repository, get_influxdb_repository
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.sensor_data import SensorDataModel
from schemas.sensor_metadata import SensorModel




router = APIRouter(tags=["sensors"])


@router.post("/sensor-data/", status_code=status.HTTP_201_CREATED)
async def add_sensor_data(sensor_data: SensorDataModel, repo=Depends(get_influxdb_repository)):
    """
    Endpoint to receive sensor data from IoT devices."""
    try:
        repo.create(sensor_data.to_influx_point())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sensor_data.model_dump()

@router.get("/sensor-data/{device_id}/{location}", status_code=status.HTTP_200_OK)
async def get_sensor_data(device_id: str, location: str, repo=Depends(get_influxdb_repository)):
    """
    Endpoint to retrieve sensor data."""
    data = repo.get_by_id(device_id, location)
    print(data)
    return data

@router.post("/sensor/",  status_code=status.HTTP_201_CREATED)
async def add_sensor(sensor: SensorModel, repo=Depends(get_sqlalchemy_repository)):
    new_sensor = repo.create(
        sensor
    )
    return new_sensor
    

@router.get("/sensor/{device_id}")
async def get_sensor_data(device_id: str, repo=Depends(get_sqlalchemy_repository)):
    sensor = repo.get_by_id(device_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor

# @router.get("/sensor-data/")
# async def get_sensor_data():
#     return {"message": "Sensor data retrieved!!!"}



