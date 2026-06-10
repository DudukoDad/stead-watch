from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field as PydanticField
from influxdb_client_3  import Point  


class SensorDataModel(BaseModel):
    measurement: Literal["homestead"] = "homestead"
    location: str
    device_id: str
    sensor_data: float = PydanticField(..., ge=-50.0, le=5000.0)
    timestamp: datetime

    def to_influx_point(self) -> Point:
        return (
            Point(self.measurement)
            .tag("location", self.location)
            .tag("device_id", self.device_id)
            .field("sensor_data", self.sensor_data)
            .time(int(self.timestamp.timestamp()))
        )

class SensorModel(BaseModel):
    device_id: int
    friendly_name: str
    location: str
    refresh_rate: str
    is_active: bool
