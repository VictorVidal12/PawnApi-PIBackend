import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from routers.pawn import dbConnect

client = TestClient(app)


def test_get_all_active_pawns(monkeypatch):
    # Arrange
    mock_get_users = AsyncMock(return_value=[{"idusuario": 1, "nombre": "Reloj", "tipo": "vigente"}])
    monkeypatch.setattr("routers.pawn.dbConnect.get_users", mock_get_users)

    # Act
    response = client.get("/pawns")  # Ajusta la ruta según tu aplicación

    # Assert
    assert response.status_code == 200
    assert response.json() == [{"idusuario": 1, "nombre": "Reloj", "tipo": "vigente"}]
    mock_get_users.assert_called_once()
