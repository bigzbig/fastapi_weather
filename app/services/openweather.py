import http
from typing import Any, Dict, Optional, Tuple

import httpx
from httpx import Response
from core.config import settings

# from weather.support import cache


class ValidationError(Exception):
    def __init__(self, error_message: str, status_code: int) -> None:
        super().__init__(error_message)
        self._status_code = status_code
        self._error_message = error_message

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def error_message(self) -> str:
        return self._error_message


class WeatherService:
    api_key: Optional[str] = settings.OPEN_WEATHER_API_KEY
    valid_units = {"standard", "metric", "imperial"}

    @classmethod
    async def report(cls, city: str, country: str, units: str) -> Optional[Dict[str, Any]]:
        city, country, units = cls._validate_units(city, country, units)

        query = f"{city},{country}"
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(url=cls._generate_url(query, cls.api_key, units))
            if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
                raise ValidationError(response.text, response.status_code)
        forecast = response.json()["main"]
        return forecast

    @staticmethod
    def _generate_url(query: str, api_key: Optional[str], units: str) -> str:
        return f"https://api.openweathermap.org/data" f"/2.5/weather?q={query}&appid={api_key}&units={units}"

    @classmethod
    def _validate_units(cls, city: str, country: Optional[str], units: str) -> Tuple[str, str, str]:
        city = city.lower().strip()
        if not country:
            country = "us"
        else:
            country = country.lower().strip()

        if len(country) != 2:
            error = f"Invalid country: {country}. " f"It must be a two letter abbreviation such as US or GB."
            raise ValidationError(status_code=int(http.HTTPStatus.BAD_REQUEST), error_message=error)

        if units:
            units = units.strip().lower()

        if units not in cls.valid_units:
            error = f'Invalid units "{units}", it must be one of {cls.valid_units}.'
            raise ValidationError(status_code=int(http.HTTPStatus.BAD_REQUEST), error_message=error)
        return city, country, units
