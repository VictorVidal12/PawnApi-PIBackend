import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMakeSellByClient(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_make_sell_by_client(self):
        image_path = "tests/sample_image.png"
        with open(image_path, "rb") as img:
            files = {"image": (image_path, img, "image/png")}

            offer_data = {
                "nombre": "Nuevo Producto",
                "descripcion": "Descripción del producto",
                "categoria": "Electrónica",
                "precio": 50000,
                "id_usuario": 1
            }


            response = self.client.post("/MakeSellByClient", data=offer_data, files=files)

            self.assertEqual(response.status_code, 404)
            self.assertIsInstance(response.json(), dict)
            self.assertIn("idOferta", response.json())
            self.assertIn("precio", response.json())
            self.assertEqual(response.json()["precio"], offer_data["precio"])


if __name__ == "__main__":
    unittest.main()
