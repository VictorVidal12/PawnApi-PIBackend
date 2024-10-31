import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAddPawn(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_add_pawn(self):
        pawn_data = {
            "precio": 100000,
            "fecha_inicio": "2024-10-22",
            "fecha_final": "2025-10-22",
            "usuario_idusuario": 1,
            "producto_idproducto": 2
        }

        response = self.client.post("/addPawn", json=pawn_data)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("idEmpennio", response.json())  # Verificar que contiene el campo id del empeño
        self.assertIn("precio", response.json())  # Verificar que contiene el precio del empeño
        self.assertIn("idFacturaEmpennio", response.json())  # Verificar que contiene el id de la factura


if __name__ == "__main__":
    unittest.main()
