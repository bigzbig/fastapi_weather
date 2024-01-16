# README

Run docker

```sh
docker compose up
```

Go to:
http://localhost:8080/docs#/Weather/weather_v1_weather__city__get


Call for example

```sh
curl 'http://0.0.0.0:8080/v1/weather/lviv?country=UA'
curl 'http://0.0.0.0:8080/v1/weather/New%20York?country=US'
curl 'http://0.0.0.0:8080/v1/weather/Washington'
curl 'http://0.0.0.0:8080/v1/weather/foo'
```

Check results in DB

```sh
sqlite3 ./app/weather.db
sqlite> select * from weather_reports;
.exit
```


Format code

```sh
docker compose run --rm fastapi ruff format .
```


