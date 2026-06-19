import os
import requests

STAGING_URL = os.getenv("STAGING_URL", "http://localhost:8001")


def test_health_endpoint_responds():
    response = requests.get(f"{STAGING_URL}/health", timeout=10)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cars_list_endpoint_responds():
    response = requests.get(f"{STAGING_URL}/api/cars/", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_retrieve_car():
    payload = {
        "brand": "IntegrationTest", "model": "X1", "year": 2024,
        "price": 30000, "fuel": "electric", "mileage": 0, "color": "Blue"
    }
    create_response = requests.post(f"{STAGING_URL}/api/cars/", json=payload, timeout=10)
    assert create_response.status_code == 201
    car_id = create_response.json()["id"]

    get_response = requests.get(f"{STAGING_URL}/api/cars/{car_id}", timeout=10)
    assert get_response.status_code == 200
    assert get_response.json()["brand"] == "IntegrationTest"