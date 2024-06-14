import requests

base_api_url = "http://127.0.0.1:8000/api"

if __name__ == '__main__':
    from_currency = "USD"
    to_currency = "RUB"
    amount = 100

    api_path = f"{base_api_url}/rates"
    api_param = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "value": amount
    }
    response = requests.get(api_path, params=api_param)

    print(response)
    print(response.text)
