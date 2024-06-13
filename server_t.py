import datetime
import json
import os
import requests

import dotenv

dotenv.load_dotenv()

rates_api_token = os.getenv("RATES_API_TOKEN")
if not rates_api_token:
    print("Error: RATES_API_TOKEN not set")
    raise Exception("Error: RATES_API_TOKEN not set")

rates_base_url = "https://api.freecurrencyapi.com/v1"
available_currencies = {}
cached_available_currencies_file = "cached_available_currencies.json"


# API: https://freecurrencyapi.com/docs/latest#request-parameters

def get_available_currencies():
    api_path = f"{rates_base_url}/currencies"
    api_param = {"apikey": rates_api_token}
    response = requests.get(api_path, params=api_param)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.reason}")
        raise Exception(f"Error: {response.status_code} - {response.reason}")

    raw_available_currencies = response.json()["data"]
    available_currencies = {
        "available_currencies": list(raw_available_currencies.keys()),
        "last_updated_at": datetime.datetime.now().timestamp()
    }

    return available_currencies


def check_available_currencies(currencies):
    if not currencies:
        return False
    elif datetime.datetime.now() - currencies["last_updated_at"] >= datetime.timedelta(days=1):
        return False
    else:
        return True


def load_cached_available_currencies():
    with open(cached_available_currencies_file, "r") as f:
        loaded_available_currencies = json.load(f)
        last_updated_at = loaded_available_currencies["last_updated_at"]
        loaded_available_currencies["last_updated_at"] = datetime.datetime.fromtimestamp(last_updated_at)

        return loaded_available_currencies


def save_cached_available_currencies(available_currencies):
    with open(cached_available_currencies_file, "w") as f:
        data_to_save = available_currencies
        data_to_save["last_updated_at"] = datetime.datetime.now().timestamp()
        json.dump(data_to_save, f)


def update_available_currencies():
    available_currencies = get_available_currencies()
    save_cached_available_currencies(available_currencies)
    return available_currencies


def load_available_currencies():
    if not os.path.exists(cached_available_currencies_file):
        available_currencies = update_available_currencies()

    else:
        available_currencies = load_cached_available_currencies()

        if not check_available_currencies(available_currencies):
            available_currencies = update_available_currencies()

    return available_currencies


def convert(from_currency, to_currency, amount):
    if from_currency == to_currency:
        return {
            "result": amount
        }

    if amount <= 0:
        return {
            "result": 0
        }

    if from_currency not in available_currencies["available_currencies"]:
        return {
            "status": 400,
            "reason": f"Invalid from_currency code . Available currencies: {available_currencies}"
        }

    if to_currency not in available_currencies["available_currencies"]:
        return {
            "status": 400,
            "reason": f"Invalid to_currency code. Available currencies: {available_currencies}"
        }

    api_path = f"{rates_base_url}/latest"
    api_headers = {}
    api_params = {
        "base_currency": from_currency,
        "currencies": [to_currency],
        "apikey": rates_api_token

    }
    response = requests.get(api_path, params=api_params, headers=api_headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.reason}")
        raise {
            "status": response.status_code,
            "reason": f"Error: {response.status_code} - {response.reason}"
        }

    response_data = response.json()
    raw_rates = response_data["data"]
    rate = raw_rates[to_currency]
    return {
        "result": round(rate * amount, 2)
    }


if __name__ == '__main__':
    available_currencies = load_available_currencies()
    print("Available currencies: ", available_currencies)

    from_currency = "USD"
    to_currency = "RUB"
    amount = 100
    result = convert(from_currency, to_currency, amount)

    print(f"{amount} {from_currency} = {result['result']} {to_currency}")
