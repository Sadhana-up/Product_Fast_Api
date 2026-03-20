from copy import deepcopy

import os
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main
from main import app

client = TestClient(app) # httpx client


@pytest.fixture(autouse=True)
def reset_products():
    original = deepcopy(main.products)
    try:
        yield
    finally:
        main.products.clear()
        main.products.extend(original)


class TestAPI:
    def test_greet(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json() == {"Hello": "World"}

    def test_get_products(self):
        r = client.get("/products")
        assert r.status_code == 200
        data = r.json()
        assert "all products" in data
        assert isinstance(data["all products"], list)
        assert len(data["all products"]) >= 3

    def test_get_product_by_id_success(self):
        r = client.get("/products/1")
        assert r.status_code == 200
        assert r.json()["id"] == 1

    def test_get_product_by_id_not_found(self):
        r = client.get("/products/999")
        assert r.status_code == 404
        assert "error" in r.json()

    def test_add_product_success(self):
        new = {"id": 100, "name": "New", "description": "d", "price": 1.0, "quantity": 2}
        r = client.post("/products", json=new)
        assert r.status_code == 201
        assert r.json()["id"] == 100
        # ensure added
        r2 = client.get("/products/100")
        assert r2.status_code == 200

    def test_add_product_conflict(self):
        new = {"id": 1, "name": "Sample Product", "description": "d", "price": 1.0, "quantity": 2}
        r = client.post("/products", json=new)
        assert r.status_code in (409, 422)

    def test_add_product_invalid_field(self):
        # negative price should trigger validation error (422)
        bad = {"id": 101, "name": "Bad", "description": "d", "price": -5.0, "quantity": 1}
        r = client.post("/products", json=bad)
        assert r.status_code == 422

    def test_update_product_success(self):
        updated = {"id": 1, "name": "Sample Product", "description": "updated", "price": 20.0, "quantity": 99}
        r = client.put("/products/1", json=updated)
        assert r.status_code == 200
        assert r.json()["description"] == "updated"

    def test_update_product_id_mismatch(self):
        updated = {"id": 999, "name": "X", "description": "d", "price": 1.0, "quantity": 1}
        r = client.put("/products/1", json=updated)
        assert r.status_code == 400

    def test_update_product_name_conflict(self):
        # try to update product 1 to have the same name as product 2
        updated = {"id": 1, "name": "Another Product", "description": "d", "price": 1.0, "quantity": 1}
        r = client.put("/products/1", json=updated)
        assert r.status_code == 409
