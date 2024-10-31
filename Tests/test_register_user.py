import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRegisterUser(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_register_user(self):
        user_data = {
            "nombre": "Nuevo Usuario",
            "correo_electronico": "nuevo.usuario@example.com",
            "contrasennia": "contraseña_segura",
            "tipo": "cliente",
            "genero": "masculino",
            "nacimiento": "2000-01-01",
            "telefono": "1234567890"
        }

        response = self.client.post("/user", json=user_data)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("idusuario", response.json())
        self.assertIn("nombre", response.json())
        self.assertEqual(response.json()["nombre"], "Nuevo Usuario")


if __name__ == "__main__":
    unittest.main()

