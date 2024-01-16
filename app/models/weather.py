from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from models.base_class import Base


class Weather(Base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    units = Column(String, nullable=False)
    temp = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp_max = Column(Float, nullable=False)
    pressure = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    sea_level = Column(Integer, nullable=True)
    grnd_level = Column(Integer, nullable=True)

    __table_args__ = (UniqueConstraint("created_at", "city", "country", "units", name="unique_weather_report"),)
