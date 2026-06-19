import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_cars_empty_or_list():
    response = client.get("/api/cars/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_car():
    payload = {
        "brand": "TestBrand", "model": "TestModel", "year": 2024,
        "price": 30000, "fuel": "petrol", "mileage": 1000, "color": "Black"
    }
    response = client.post("/api/cars/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["brand"] == "TestBrand"
    assert "id" in data


def test_get_nonexistent_car_returns_404():
    response = client.get("/api/cars/999999")
    assert response.status_code == 404


def test_create_car_missing_field_fails():
    payload = {"brand": "Incomplete"}
    response = client.post("/api/cars/", json=payload)
    assert response.status_code == 422

def test_create_car_negative_price_fails():
    payload = {
        "brand": "TestBrand", "model": "TestModel", "year": 2024,
        "price": -500, "fuel": "petrol", "mileage": 1000, "color": "Black"
    }
    response = client.post("/api/cars/", json=payload)
    assert response.status_code == 422   