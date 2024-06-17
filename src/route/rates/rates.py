import datetime

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response
from starlette.exceptions import HTTPException

from models import ConvertRatesReturnModel
from route.rates import freecurrency_api
from redis_server import get_redis

rates_router = APIRouter()


@rates_router.get("/rates", status_code=status.HTTP_200_OK, response_model=ConvertRatesReturnModel)
def convert(from_currency: str, to_currency: str, value: float):
    print(f"from_currency: {from_currency}, to_currency: {to_currency}, value: {value}")
    if from_currency == to_currency:
        return {"result": value}

    if value <= 0:
        return {"result": 0.0}

    redis = get_redis()
    cache_rates = redis.get(f'{from_currency}_{to_currency}')
    if cache_rates:
        print("Cache hit")
        rates = float(cache_rates)
        convert_result = round(rates * value, 2)
        return {"result": convert_result}
    else:
        print("Cache miss")

    rates = freecurrency_api.convert_currency_rates(from_currency, to_currency, value)
    convert_result = round(rates, 2)

    if redis:
        redis.set(f"{from_currency}_{to_currency}", rates, ex=datetime.timedelta(days=1))
        print("Cache set")

    print(f"converted_value: {convert_result}")
    return {"result": convert_result}
