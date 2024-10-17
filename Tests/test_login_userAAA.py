import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


class TestLoginUser(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("routers.user.dbConnect.get_user_by_email")
    @patch("routers.user.create_jwt_token")
    def test_login_user_success(self, mock_create_jwt_token, mock_get_user_by_email):
        # Arrange
        email = "test@example.com"
        password = "correct_password"
        user_data = {
            "correo_electronico": email,
            "contrasennia": password,
            "nacimiento": "1990-01-01"
        }
        mock_get_user_by_email.return_value = user_data
        mock_create_jwt_token.return_value = "mocked_token"

        # Act
        response = self.client.post("/login", json={"email": email, "password": password})

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "data": user_data,
            "token": "mocked_token"
        })

    @patch("routers.user.dbConnect.get_user_by_email")
    def test_login_user_incorrect_password(self, mock_get_user_by_email):
        # Arrange
        email = "test@example.com"
        password = "incorrect_password"
        user_data = {
            "correo_electronico": email,
            "contrasennia": "correct_password",
            "nacimiento": "1990-01-01",
        }
        mock_get_user_by_email.return_value = user_data

        # Act
        response = self.client.post("/login", json={"email": email, "password": password})

        # Assert
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"detail": "Incorrect password"})

    @patch("routers.user.dbConnect.get_user_by_email")
    def test_login_user_not_found(self, mock_get_user_by_email):
        # Arrange
        email = "test@example.com"
        password = "some_password"
        mock_get_user_by_email.return_value = None  # Usuario no encontrado

        # Act
        response = self.client.post("/login", json={"email": email, "password": password})

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "user does not found"})


if __name__ == "__main__":
    unittest.main()

