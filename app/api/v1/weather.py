import http

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from schemas.weather import LocationInpt, WeatherOut
from services import openweather
from crud.weather import create_weather_report
from core.db import get_db


router = APIRouter(prefix="/v1/weather", tags=["Weather"])


@router.get("/{city}")
async def weather(
    location: LocationInpt = Depends(), units: str = "metric", db: Session = Depends(get_db)
) -> WeatherOut:
    """Returns a city weather route."""
    try:
        result = await openweather.WeatherService.report(location.city, location.country, units)
        weather_result = WeatherOut(city=location.city, country=location.country, units=units, **result)

        if result:
            create_weather_report(weather_result, db=db)

        return weather_result
    except openweather.ValidationError as err:
        raise HTTPException(detail=err.error_message, status_code=err.status_code)
    except Exception as err:
        raise HTTPException(
            detail=str(err),
            status_code=int(http.HTTPStatus.INTERNAL_SERVER_ERROR),
        )
