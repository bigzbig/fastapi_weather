import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "FastAPI Service 🔥"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL = "sqlite:///./weather.db"

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    OPEN_WEATHER_API_KEY: str = os.getenv("OPEN_WEATHER_API_KEY")


settings = Settings()
