import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMakePawnByClient(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_make_pawn_by_client(self):
        image_path = "tests/sample_image.png"
        with open(image_path, "rb") as img:
            files = {"image": (image_path, img, "image/png")}

            pawn_data = {
                "nombre": "Producto Empeño",
                "descripcion": "Descripción del producto empeñado",
                "categoria": "Electrónica",
                "precio": 30000,
                "id_usuario": 1
            }

            response = self.client.post("/MakePawnByClient", data=pawn_data, files=files)

            self.assertEqual(response.status_code, 402)
            self.assertIsInstance(response.json(), dict)
            self.assertIn("idOferta", response.json())
            self.assertIn("precio", response.json())
            self.assertEqual(response.json()["precio"], pawn_data["precio"])


if __name__ == "__main__":
    unittest.main()
