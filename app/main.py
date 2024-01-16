from api.v1 import weather
from fastapi import FastAPI
from api.v1 import authentication, user
from core.db import init_db


app = FastAPI()

init_db()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(weather.router)
