from pydantic import BaseModel


class Product(BaseModel):
    idArticulo: int | None
    imagen: str
    nombre: str
    valorReal: int | None
    descripcion: int
    categoria: str
