from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

# Datos de ejemplo para las pruebas
valid_user = {
    "correo_electronico": "test@example.com",
    "contrasennia": "correct_password",
    "nacimiento": "1990-01-01"
}

invalid_password_user = {
    "correo_electronico": "test@example.com",
    "contrasennia": "wrong_password",
    "nacimiento": "1990-01-01"
}


# 1. Test para login exitoso
@patch("db.dbConnector.ConnectionDB.get_user_by_email")
@patch("tools.token.create_jwt_token")
def test_login_success(mock_create_token, mock_get_user_by_email):
    # Arrange: Configuramos los mocks
    mock_get_user_by_email.return_value = valid_user
    mock_create_token.return_value = "fake_jwt_token"

    login_data = {
        "email": "test@example.com",
        "password": "correct_password"
    }

    # Act: Hacemos la petición POST a la ruta /login
    response = client.post("/user/login", json=login_data)

    # Assert: Verificamos el resultado
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
    assert response.json()["token"] == "fake_jwt_token"


# 2. Test para login con contraseña incorrecta
@patch("db.dbConnector.ConnectionDB.get_user_by_email")
def test_login_incorrect_password(mock_get_user_by_email):
    # Arrange
    mock_get_user_by_email.return_value = invalid_password_user

    login_data = {
        "email": "test@example.com",
        "password": "wrong_password"
    }

    # Act
    response = client.post("/user/login", json=login_data)

    # Assert
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json()["detail"] == "Incorrect password"


# 3. Test para login con usuario no encontrado
@patch("db.dbConnector.ConnectionDB.get_user_by_email")
def test_login_user_not_found(mock_get_user_by_email):
    # Arrange
    mock_get_user_by_email.return_value = None

    login_data = {
        "email": "non_existent_user@example.com",
        "password": "any_password"
    }

    # Act
    response = client.post("/user/login", json=login_data)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "user does not found"
