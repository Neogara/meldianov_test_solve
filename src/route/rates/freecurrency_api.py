import datetime
import json
import os
import requests
from starlette import status
from starlette.responses import Response
from starlette.exceptions import HTTPException
from dotenv import load_dotenv

load_dotenv()
# API: https://freecurrencyapi.com/docs/latest#request-parameters

base_url = "https://api.freecurrencyapi.com/v1"
api_token = os.getenv("RATES_API_TOKEN")
if not api_token:
    print("Error: RATES_API_TOKEN not set")
    raise EnvironmentError("Error: RATES_API_TOKEN not set")


def get_available_currencies():
    api_path = f"{base_url}/currencies"
    api_param = {"apikey": api_token}
    response = requests.get(api_path, params=api_param)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.reason)

    raw_available_currencies = response.json()["data"]
    available_currencies = {
        "available_currencies": list(raw_available_currencies.keys()),
        "last_updated_at": datetime.datetime.now().timestamp()
    }

    return available_currencies


def convert_currency_rates(from_currency, to_currency, amount):
    api_path = f"{base_url}/latest"
    api_headers = {}
    api_params = {
        "base_currency": from_currency,
        "currencies": [to_currency],
        "apikey": api_token

    }
    response = requests.get(api_path, params=api_params, headers=api_headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.reason)

    response_data = response.json()
    raw_rates = response_data["data"]

    rate = raw_rates[to_currency]
    return rate

# if __name__ == '__main__':
#     available_currencies = load_available_currencies()
#     print("Available currencies: ", available_currencies)
#
#     from_currency = "USD"
#     to_currency = "RUB"
#     amount = 100
#     result = convert_rates(from_currency, to_currency, amount)
#
#     print(f"{amount} {from_currency} = {result['result']} {to_currency}")
