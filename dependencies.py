import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

from models import Base
from repositories import SensorRepository, InfluxClientRepository, Repository, UserRepository
# Load the env variables
load_dotenv()

def get_sqlalchemy_repository():
    """"
    Factory function to create a SQLAlchemy repository instance.
    Reads database configuration from environment variables and initializes the repository.
    """
    db_host = os.getenv("db_host")
    db_port = os.getenv("db_port")
    db_user = os.getenv("db_user")
    db_password = os.getenv("db_password")
    db_name = os.getenv("db_name")

    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    print("*"*10)
    print(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return SensorRepository(Session())

def get_influxdb_repository():
    """"
    Factory function to create a InfluxDB repository instance.
    Reads token and other configuration from environment variables and initializes the repository.
    """
    token = os.getenv("influxdb_token")
    org = os.getenv("influxdb_org")
    bucket = os.getenv("influxdb_bucket")
    host = os.getenv("influxdb_host")
    port = os.getenv("influxdb_port")

    return InfluxClientRepository(token, org, bucket, host, port)

def get_sqllite_repository(repository_type: Repository):
    db_name = os.getenv("db_name", "stead_watch.db")

    base_dir = Path(__file__).resolve().parent
    db_path = (base_dir / db_name).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(f"sqlite:///{db_path.as_posix()}")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return repository_type(Session())


def get_user_repository():
    return get_sqllite_repository(UserRepository)

def get_sensor_repository():
    return get_sqllite_repository(SensorRepository)