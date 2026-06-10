from influxdb_client_3 import InfluxDBClient3, Point
from sqlalchemy.orm import Session
from models import Sensor
from abc import ABC, abstractmethod

class SensorRepository(ABC):
    @abstractmethod
    def get_by_id(self, device_id: str):
        pass
    @abstractmethod
    def create(self, sensor: Sensor) -> None:
        pass
    @abstractmethod
    def exists(self) -> bool:
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
    
    def exists(self, device_id: str) -> bool:
        return self.session.query(Sensor).filter(Sensor.device_id == device_id).first() is not None
    
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
    

class InfluxClientRepository(SensorRepository):
    """ A simple wrapper around the InfluxDBClient to handle writing and querying data. """
    def __init__(self,token,org, database, host, port): 
        self.database = database
        self._client = InfluxDBClient3(
                        host=f"http://{host}:{port}",
                        token=token,
                        org=org,
                        database=database,
                        auth_scheme="Bearer"
                        )
        # self._client = InfluxDBClient3(url=f"http://{host}:{port}", token=token)


    def create(self, sensor_data: Point) -> None:
        """ Write Data to InfluxDB using the provided write option (SYNCHRONOUS or ASYNCHRONOUS)"""

        # write_api = self._client.write_api(write_option)
        print(sensor_data)
        r = self._client.write( record=sensor_data)
        print(r)

    def get_by_id(self,id: str, location: str) -> list[tuple]:
        measurement_name = 'homestead'
        target_id = id
        # Construct the SQL query
        # Note: replace 'id_column_name' with your actual tag or field name for the ID
        query = f"SELECT * FROM {measurement_name} WHERE device_id = '{target_id}'"

        # Execute the query and convert to a Pandas DataFrame
        table = self._client.query(query)
        df = table.to_pandas()
        return df.to_dict(orient='records')
    
    def exists(self, id: str) -> bool:
        measurement_name = 'homestead'
        target_id = id
        query = f"SELECT COUNT(*) FROM {measurement_name} WHERE device_id = '{target_id}'"
        table = self._client.query(query)
        df = table.to_pandas()
        count = df.iloc[0, 0]  # Assuming the count is in the first row and first column
        return count > 0