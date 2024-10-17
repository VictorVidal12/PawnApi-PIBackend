import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from routers.sale import dbConnect

client = TestClient(app)


def test_get_user_sale_requests(monkeypatch):
    # Arrange
    mock_get_user_sale_requests = AsyncMock(
        return_value=[{"id": 1, "user_id": 2, "item": "Laptop", "status": "pendiente"}])
    monkeypatch.setattr("routers.sale.dbConnect.get_user_sale_requests", mock_get_user_sale_requests)

    # Act
    response = client.get("/sales/requests")

    # Assert
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "user_id": 2, "item": "Laptop", "status": "pendiente"}]
    mock_get_user_sale_requests.assert_called_once()
