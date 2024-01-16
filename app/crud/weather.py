from sqlalchemy.orm import Session
from models.weather import Weather
from schemas.weather import WeatherOut
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_weather_report(wather: WeatherOut, db: Session):
    now = datetime.now()
    date_now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    data = wather.dict()
    data["city"] = data["city"].lower()
    item = Weather(created_at=date_now, **data)
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    db.refresh(item)
    return item
