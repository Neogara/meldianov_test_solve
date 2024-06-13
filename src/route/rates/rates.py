from fastapi import APIRouter
from starlette import status
from starlette.responses import Response
from starlette.exceptions import HTTPException

from models import ConvertRatesReturnModel
from route.rates import freecurrency_api

rates_router = APIRouter()


@rates_router.get("/rates", status_code=status.HTTP_200_OK, response_model=ConvertRatesReturnModel)
def convert(from_currency: str, to_currency: str, value: float):
    print(f"from_currency: {from_currency}, to_currency: {to_currency}, value: {value}")
    converted_currency_value = freecurrency_api.convert_currency_rates(from_currency, to_currency, value)

    print(f"converted_value: {converted_currency_value}")

    return {
        "result": round(converted_currency_value, 2)
    }
