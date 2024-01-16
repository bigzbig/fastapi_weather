from typing import Optional
from pydantic import BaseModel


class LocationInpt(BaseModel):
    city: str
    country: str = "US"


class WeatherOut(BaseModel):
    city: str
    country: str
    units: str
    temp: Optional[float] = None
    feels_like: Optional[float] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    class Config:
        from_attributes = True
