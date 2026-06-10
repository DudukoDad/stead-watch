from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import Session
from models.sensor_metadata_model import Sensor
from abc import ABC, abstractmethod
from typing import List, Optional

class SensorRepository(ABC):
    @abstractmethod
    def get_by_id(self, device_id: str) -> Optional[Sensor]:
        pass
    @abstractmethod
    def create(self, sensor: Sensor) -> None:
        pass
    @abstractmethod
    def get_all(self) -> List[Sensor]:
        pass


class SqlAlchemySensorRepository(SensorRepository):
    def __init__(self, session: Session):
        self.session = session

        
    def get_all(self) -> list[Sensor]:
        return self.session.query(Sensor).all()

    def get_by_id(self, device_id: str) -> Sensor | None:
        return self.session.query(Sensor).filter(Sensor.device_id == device_id).first()

    def get_by_location(self, location: str) -> list[Sensor]:
        return self.session.query(Sensor).filter(Sensor.location == location).all()

    def create(self, sensor: Sensor) -> Sensor:
        sensor = Sensor(**sensor.dict())
        self.session.add(sensor)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def update(self, device_id: str, **kwargs) -> Sensor | None:
        sensor = self.get_by_id(device_id)
        if not sensor:
            return None
        for key, value in kwargs.items():
            setattr(sensor, key, value)
        self.session.commit()
        self.session.refresh(sensor)
        return sensor

    def delete(self, device_id: str) -> bool:
        sensor = self.get_by_id(device_id)
        if not sensor:
            return False
        self.session.delete(sensor)
        self.session.commit()
        return True