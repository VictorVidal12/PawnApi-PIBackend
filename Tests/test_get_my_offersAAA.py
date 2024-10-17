import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from routers.pawn import dbConnect

client = TestClient(app)


# Test para el endpoint /clientCurrentPawns/{id}
def test_get_client_current_pawns(monkeypatch):
    # Arrange
    client_id = 1
    expected_pawns = [{"id": 1, "status": "active"}, {"id": 2, "status": "active"}]

    mock_get_pawns = AsyncMock(return_value=expected_pawns)
    monkeypatch.setattr("routers.pawn.dbConnect.get_currents_pawns_by_userid", mock_get_pawns)

    mock_change_datetime = AsyncMock(return_value=expected_pawns)
    monkeypatch.setattr("routers.pawn.change_datetime_to_str", mock_change_datetime)

    # Act
    response = client.get(f"/clientCurrentPawns/{client_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_pawns
    mock_get_pawns.assert_called_once_with(client_id)
    mock_change_datetime.assert_called_once_with(expected_pawns)

