import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app
from routers.user import dbConnect

client = TestClient(app)


def test_register_user(monkeypatch):
    # Arrange
    user_data = {
        "nombre": "Nuevo Usuario",
        "correo_electronico": "nuevo.usuario@example.com",
        "contrasennia": "contraseña_segura",
        "tipo": "cliente",
        "genero": "masculino",
        "nacimiento": "2000-01-01",
        "telefono": "1234567890"
    }
    mock_add_user = AsyncMock(return_value={"idusuario": 1, "nombre": "Nuevo Usuario"})
    monkeypatch.setattr("routers.user.dbConnect.add_user", mock_add_user)

    # Act
    response = client.post("/user", json=user_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"idusuario": 1, "nombre": "Nuevo Usuario"}
    mock_add_user.assert_called_once_with(
        nombre="Nuevo Usuario",
        correo_electronico="nuevo.usuario@example.com",
        contrasennia="contraseña_segura",
        tipo="cliente",
        genero="masculino",
        nacimiento="2000-01-01",
        telefono="1234567890"
    )
