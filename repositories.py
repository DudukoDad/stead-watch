from influxdb_client_3 import InfluxDBClient3, Point
from sqlalchemy.orm import Session
from schemas import UserInDB, UserCreate
from models import User, Sensor, Base
from abc import ABC, abstractmethod
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


class Repository(ABC):
    def __init__(self, session: Session, model: Base):
        self.session = session
        self.model = model
    @abstractmethod
    def get_by_id(self, id: str):
        pass
    @abstractmethod
    def create(self,) -> None:
        pass
    @abstractmethod
    def exists(self, id) -> bool:
        pass

class BaseRepository(Repository):
    def get_all(self) -> list[Base]:
            return self.session.query(self.model).all()
    def get_by_id(self, id: str) -> Base | None:
            return self.session.query(self.model).filter(self.model.id == id).first()
    
    def create(self, sql_alch_model: Base) -> Base:
            print(sql_alch_model.__repr__)
            print(sql_alch_model.dict())
            new_record = self.model(**sql_alch_model.dict())
            self.session.add(new_record)
            self.session.commit()
            self.session.refresh(new_record)
            return new_record
    
    def exists(self, id: str) -> bool:
            return self.session.query(self.model).filter(self.model.id == id).first() is not None
    
    def update(self, id: str, **kwargs) -> Base | None:
            target_record = self.get_by_id(id)
            if not target_record:
                return None
            for key, value in kwargs.items():
                setattr(target_record, key, value)
            self.session.commit()
            self.session.refresh(target_record)
            return target_record
    
    def delete(self, id: str) -> bool:
            target_record = self.get_by_id(id)
            if not target_record:
                return False
            self.session.delete(target_record)
            self.session.commit()
            return True

class SensorRepository(BaseRepository):
    def __init__(self, session: Session):
            self.session = session
            self.model = Sensor
    def get_by_location(self, location: str) -> list[Sensor]:
            return self.session.query(Sensor).filter(Sensor.location == location).all()
    def get_by_user_id(self, user_id: int) -> list[Sensor]:
            return self.session.query(Sensor).filter(Sensor.user_id == user_id).all()

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session
        self.model = User

    def _get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)
    
    def create(self, user: UserCreate) -> UserInDB:
                user_data = user.model_dump(exclude={"password"})
                user_data["hashed_password"] = self._get_password_hash(user.password)

                new_record = self.model(**user_data)
                print(new_record)
                
                self.session.add(new_record)
                self.session.commit()
                self.session.refresh(new_record)
                returnable_keys = ['username', 'role', 'email', 'full_name' ]
                new_record = {key: getattr(new_record, key) for key in returnable_keys}
                return new_record
    def get_by_username(self, username: str) -> Base | None:
                return self.session.query(self.model).filter(self.model.username == username).first()
    def exists(self, username: str) -> bool:
                return self.session.query(self.model).filter(self.model.username == username).first() is not None

class InfluxClientRepository(Repository):
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

    def get_by_id(self, device_id: str) -> list[tuple]:
        measurement_name = 'homestead'
        target_id = device_id
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


    
