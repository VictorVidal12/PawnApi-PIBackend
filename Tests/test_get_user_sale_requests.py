import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestGetUserSaleRequests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_user_sale_requests(self):
        response = self.client.get("/sales/requests")
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json(), list)
        if len(response.json()) > 0:
            self.assertIn("id", response.json()[0])
            self.assertIn("user_id", response.json()[0])
            self.assertIn("item", response.json()[0])
            self.assertIn("status", response.json()[0])


if __name__ == "__main__":
    unittest.main()
