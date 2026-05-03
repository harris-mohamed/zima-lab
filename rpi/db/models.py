from datetime import datetime

from sqlalchemy import Float, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    arduino_ts: Mapped[int] = mapped_column(Integer, nullable=False)
    plant_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    ph: Mapped[float | None] = mapped_column(Float, nullable=True)
    tds: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_temp: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_level_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    air_temp: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
