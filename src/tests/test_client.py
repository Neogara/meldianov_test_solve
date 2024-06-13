from service_app import app
from fastapi.testclient import TestClient

test_client = TestClient(app)


def test_convert():
    api_path = f"api/rates"

    response = test_client.get(api_path, params={
        "from_currency": "USD",
        "to_currency": "RUB",
        "value": 100
    })
    assert response.status_code == 200


def test_bad_request():
    api_path = f"api/rates"
    response = test_client.get(api_path, params={
        "from_currency": "USD",
        "to_currency": "RUS",
        "value": 100
    })
    assert response.status_code == 422
    assert response.json() == {"detail": "Unprocessable Content"}


def test_zero_value():
    api_path = f"api/rates"
    response = test_client.get(api_path, params={
        "from_currency": "USD",
        "to_currency": "RUB",
        "value": 0
    })
    assert response.status_code == 200
    assert response.json() == {"result": 0.0}


def test_zero_less_value():
    api_path = f"api/rates"
    response = test_client.get(api_path, params={
        "from_currency": "USD",
        "to_currency": "RUS",
        "value": -2
    })
    assert response.status_code == 200
    assert response.json() == {"result": 0.0}


def test_bad_value():
    api_path = f"api/rates"
    response = test_client.get(api_path, params={
        "from_currency": "USD",
        "to_currency": "RUS",
        "value": "abc"
    })
    assert response.status_code == 422
