import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestClientBuyAndShopSell(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_add_client_buy_and_shop_sell(self):
        buy_data = {
            "precio": 50000,
            "fecha": "2024-10-22",
            "usuario_idusuario": 1,
            "producto_idproducto": 10
        }

        bill_data = {
            "nombres": "John",
            "apellidos": "Doe",
            "direccion": "123 Main St",
            "departamento": "Antioquia",
            "municipio": "Medellin",
            "telefono": "3001234567",
            "correo": "johndoe@example.com"
        }

        response = self.client.post("/client", json={"buy": buy_data, "bill": bill_data})

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("idCompra", response.json())
        self.assertIn("precio", response.json())
        self.assertEqual(response.json()["precio"], buy_data["precio"])

    def test_add_client_buy_and_shop_sell_with_shop_id(self):
        buy_data = {
            "precio": 50000,
            "fecha": "2024-10-22",
            "usuario_idusuario": 8,
            "producto_idproducto": 10
        }

        bill_data = {
            "nombres": "John",
            "apellidos": "Doe",
            "direccion": "123 Main St",
            "departamento": "Antioquia",
            "municipio": "Medellin",
            "telefono": "3001234567",
            "correo": "johndoe@example.com"
        }

        response = self.client.post("/client", json={"buy": buy_data, "bill": bill_data})

        self.assertEqual(response.status_code, 405)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "The buyer client id cannot be the same that the shop (8)")


if __name__ == "__main__":
    unittest.main()
