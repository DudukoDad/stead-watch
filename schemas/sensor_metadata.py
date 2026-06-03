from pydantic import BaseModel


class SensorModel(BaseModel):
    device_id: int
    friendly_name: str
    location: str
    refresh_rate: str
    is_active: bool
