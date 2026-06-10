from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "sensor_info"
    __table_args__ = {"schema": "data"}

    device_id: Mapped[int] = mapped_column(primary_key=True)
    friendly_name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    # This will be in Cron Format e.g. "*/5 * * * *" for every 5 minutes
    refresh_rate: Mapped[str] = mapped_column(String(50), nullable=False)
    create_time: Mapped[datetime] = mapped_column(default=datetime.now())
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"Sensor(device_id={self.device_id}, location='{self.location}', refresh_rate='{self.refresh_rate}', create_time='{self.create_time}', is_active={self.is_active})"

    

   