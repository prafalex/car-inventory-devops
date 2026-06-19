import os
import time
import requests

STAGING_URL = os.getenv("STAGING_URL", "http://car_backend_staging:8000")


def wait_for_backend(timeout=30):
    """Give the backend a moment in case this test runs right after deploy."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = requests.get(f"{STAGING_URL}/health", timeout=3)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)
    return False


def test_backend_is_reachable():
    assert wait_for_backend(), f"Backend at {STAGING_URL} did not become ready in time"


def test_health_endpoint_responds():
    response = requests.get(f"{STAGING_URL}/health", timeout=10)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "car-inventory-backend"


def test_cars_list_endpoint_responds():
    response = requests.get(f"{STAGING_URL}/api/cars/", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_car():
    payload = {
        "brand": "IntegrationTest",
        "model": "X1",
        "year": 2024,
        "price": 30000,
        "fuel": "electric",
        "mileage": 0,
        "color": "Blue",
    }
    response = requests.post(f"{STAGING_URL}/api/cars/", json=payload, timeout=10)
    assert response.status_code == 201
    data = response.json()
    assert data["brand"] == "IntegrationTest"
    assert "id" in data


def test_create_then_retrieve_car():
    payload = {
        "brand": "IntegrationTest",
        "model": "X2",
        "year": 2024,
        "price": 35000,
        "fuel": "hybrid",
        "mileage": 100,
        "color": "Red",
    }
    create_response = requests.post(f"{STAGING_URL}/api/cars/", json=payload, timeout=10)
    assert create_response.status_code == 201
    car_id = create_response.json()["id"]

    get_response = requests.get(f"{STAGING_URL}/api/cars/{car_id}", timeout=10)
    assert get_response.status_code == 200
    assert get_response.json()["model"] == "X2"


def test_create_car_negative_price_rejected():
    payload = {
        "brand": "IntegrationTest",
        "model": "Invalid",
        "year": 2024,
        "price": -500,
        "fuel": "petrol",
        "mileage": 0,
        "color": "Black",
    }
    response = requests.post(f"{STAGING_URL}/api/cars/", json=payload, timeout=10)
    assert response.status_code == 422


def test_get_nonexistent_car_returns_404():
    response = requests.get(f"{STAGING_URL}/api/cars/999999", timeout=10)
    assert response.status_code == 404


def test_delete_car():
    payload = {
        "brand": "ToDelete",
        "model": "Temp",
        "year": 2024,
        "price": 15000,
        "fuel": "petrol",
        "mileage": 0,
        "color": "Gray",
    }
    create_response = requests.post(f"{STAGING_URL}/api/cars/", json=payload, timeout=10)
    car_id = create_response.json()["id"]

    delete_response = requests.delete(f"{STAGING_URL}/api/cars/{car_id}", timeout=10)
    assert delete_response.status_code == 204

    get_response = requests.get(f"{STAGING_URL}/api/cars/{car_id}", timeout=10)
    assert get_response.status_code == 404