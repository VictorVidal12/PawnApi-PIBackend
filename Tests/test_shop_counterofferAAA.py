import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from routers.offer import dbConnect


class TestShopCounteroffer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("routers.offer.dbConnect.shop_counteroffer")
    def test_shop_counteroffer_success(self, mock_shop_counteroffer):
        # Arrange
        id = 1
        precio = 100
        expected_offer = {"id": id, "precio": precio, "status": "counteroffer accepted"}
        mock_shop_counteroffer.return_value = expected_offer

        # Act
        response = self.client.put(f"/shop_counteroffer?id={id}&precio={precio}")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_offer)
        mock_shop_counteroffer.assert_called_once_with(id, precio)

    @patch("routers.offer.dbConnect.shop_counteroffer")
    def test_shop_counteroffer_not_found(self, mock_shop_counteroffer):
        # Arrange
        id = 999  # Assuming this ID does not exist
        precio = 100
        mock_shop_counteroffer.side_effect = Exception("Offer not found")

        # Act
        response = self.client.put(f"/shop_counteroffer?id={id}&precio={precio}")

        # Assert
        self.assertEqual(response.status_code, 404)  # Assuming you want to return 404 for not found
        self.assertIn("detail", response.json())  # Check if a detail key exists in response


if __name__ == "__main__":
    unittest.main()