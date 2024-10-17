import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from routers.offer import dbConnect


class TestUpdateOfferState(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_update_offer_state_finalizada(self):
        # Arrange
        id = 8
        state = "finalizada"
        id_acceptant = 2

        # Act
        response = self.client.put(f"/update_offer_state?id={id}&state={state}&id_acceptant={id_acceptant}")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": id, "state": "finalizada", "id_acceptant": id_acceptant})

    @patch("routers.offer.dbConnect.update_offer_state")
    def test_update_offer_state_other_states(self, mock_update_offer_state):
        # Arrange
        id = 8
        state = "en_curso"
        mock_update_offer_state.return_value = {"id": id, "state": state}

        # Act
        response = self.client.put(f"/update_offer_state?id={id}&state={state}")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": id, "state": state})
        mock_update_offer_state.assert_called_once_with(id, state)


if __name__ == "__main__":
    unittest.main()

