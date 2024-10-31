import unittest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app


class TestGetAllActivePawns(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("routers.pawn.dbConnect.get_users", new_callable=AsyncMock)
    def test_get_all_active_pawns(self, mock_get_users):
        # Arrange
        mock_get_users.return_value = [{"idusuario": 1, "nombre": "Reloj", "tipo": "vigente"}]
        # Act
        response = self.client.get("/pawns")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"idusuario": 1, "nombre": "Reloj", "tipo": "vigente"}])
        mock_get_users.assert_called_once()


if __name__ == "__main__":
    unittest.main()
