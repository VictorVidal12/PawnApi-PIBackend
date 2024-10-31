import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


class TestAddBillPawn(unittest.TestCase):

    @patch('routers.bill.dbConnect.add_bill_pawn')
    @patch('routers.bill.check_payment_method')
    @patch('routers.bill.check_department')
    def test_add_bill_success(self, mock_check_department, mock_check_payment_method, mock_add_bill_pawn):
        # Arrange
        mock_check_payment_method.return_value = "valid_payment_method"
        mock_check_department.return_value = "valid_department"
        mock_add_bill_pawn.return_value = {"id": 1, "municipio": "test_municipio"}

        bill_data = {
            "telefono": "1234567890",
            "municipio": "Test_Municipio",
            "medio_pago": "credit_card",
            "departamento": "Test_Departamento",
            "idFacturaEmpennio": 123
        }

        # Act
        response = client.post("/BillPawn", json=bill_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"id": 1, "municipio": "test_municipio"})
        mock_add_bill_pawn.assert_called_once_with(
            telefono="1234567890",
            municipio="test_municipio",
            medio_pago="valid_payment_method",
            departamento="valid_department"
        )

    @patch('routers.bill.check_payment_method')
    @patch('routers.bill.check_department')
    def test_add_bill_invalid_phone(self):
        bill_data = {
            "telefono": "12345",
            "municipio": "Test_Municipio",
            "medio_pago": "credit_card",
            "departamento": "Test_Departamento",
            "idFacturaEmpennio": 123
        }

        response = client.post("/BillPawn", json=bill_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Phone is invalid", response.json()["detail"])

    @patch('routers.bill.dbConnect.add_bill_pawn')
    @patch('routers.bill.check_payment_method')
    @patch('routers.bill.check_department')
    def test_add_bill_not_found(self, mock_check_department, mock_check_payment_method, mock_add_bill_pawn):
        mock_check_payment_method.return_value = "valid_payment_method"
        mock_check_department.return_value = "valid_department"
        mock_add_bill_pawn.return_value = None

        bill_data = {
            "telefono": "1234567890",
            "municipio": "Test_Municipio",
            "medio_pago": "credit_card",
            "departamento": "Test_Departamento",
            "idFacturaEmpennio": 123
        }

        response = client.post("/BillPawn", json=bill_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Cannot create the pawn bill", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
