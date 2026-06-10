import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Base
from repositories import SqlAlchemySensorRepository
from repositories import InfluxClientRepository
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
    return SqlAlchemySensorRepository(Session())

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