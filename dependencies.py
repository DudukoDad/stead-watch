import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.sensor_metadata_model import Base
from repositories.sensor_metadata_repo import SqlAlchemySensorRepository
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