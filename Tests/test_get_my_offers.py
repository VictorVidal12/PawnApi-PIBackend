import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestClientCurrentPawns(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_client_current_pawns(self):
        client_id = 1
        response = self.client.get(f"/clientCurrentPawns/{client_id}")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json(), list)
        if len(response.json()) > 0:
            pawn = response.json()[0]
            self.assertIn("id", pawn)
            self.assertIn("status", pawn)

if __name__ == "__main__":
    unittest.main()
