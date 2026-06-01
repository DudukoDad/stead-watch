from datetime import datetime
from typing import Literal, Dict, Any
from pydantic import BaseModel, Field as PydanticField
from influxdb_client import InfluxDBClient, Point

# 1. Define your data validation layout using Pydantic
class SensorModel(BaseModel):
    measurement: Literal["homestead"] = "homestead"
    
    # Tags (Metadata for indexing)
    location: str
    device_id: str
    
    # I know its pretty generic TODO: come up with a better schema for the sensor data
    sensor_data: float = PydanticField(..., ge=-50.0, le=60.0)

    
    # Timestamp
    timestamp: datetime = PydanticField(default_factory=datetime.utcnow)

    # Helper method to transform Pydantic object directly into an InfluxDB Point
    def to_influx_point(self) -> Point:
        point = Point(self.measurement).time(self.timestamp)
        
        # Add indexing tags
        point.tag("location", self.location)
        point.tag("device_id", self.device_id)
        
        # Add scalar values
        point.field("sensor_data", self.sensor_data)

        return point