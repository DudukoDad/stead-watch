from datetime import datetime
from typing import Dict

from dependencies import get_sqlalchemy_repository, get_influxdb_repository, get_sensor_repository
from fastapi import APIRouter, Depends, HTTPException, status

from schemas import SensorDataModel
from schemas import SensorModel




router = APIRouter(tags=["sensors"])


@router.post("/sensor-data/", status_code=status.HTTP_201_CREATED)
async def add_sensor_data(sensor_data: SensorDataModel, repo=Depends(get_influxdb_repository)):
    """
    Endpoint to receive sensor data from IoT devices."""
    device = get_sqlalchemy_repository().get_by_id(sensor_data.device_id)  # Check if sensor exists
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    try:
        repo.create(sensor_data.to_influx_point())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return sensor_data.model_dump()

# @router.get("/sensor-data/")
# async def get_sensor_data():
#     return {"message": "Sensor data retrieved!!!"}

@router.get("/sensor-data/{device_id}", status_code=status.HTTP_200_OK)
async def get_sensor_data(device_id: str, repo=Depends(get_influxdb_repository)):
    """
    Endpoint to retrieve sensor data."""
    if not repo.exists(device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    
    try:
        data = repo.get_by_id(device_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    if not data:        
        raise HTTPException(status_code=404, detail="No data found for this device")
    
    return data.model_dump()

@router.post("/sensor/",  status_code=status.HTTP_201_CREATED)
async def add_sensor(sensor: SensorModel, repo=Depends(get_sensor_repository)):
    if repo.exists(sensor.device_id):
        raise HTTPException(status_code=400, detail="Device with this ID already exists")
    try:
        new_sensor = repo.create(sensor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print("shit")
    return new_sensor.model_dump()
    

@router.get("/sensor/{device_id}")
async def get_sensor_data(device_id: str, repo=Depends(get_sensor_repository)):
    if not repo.exists(device_id):
        raise HTTPException(status_code=404, detail="Device not found")
    
    try:
        sensor = repo.get_by_id(device_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(type(sensor))
    return sensor


