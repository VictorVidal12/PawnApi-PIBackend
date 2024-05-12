from pydantic import BaseModel

class Product(BaseModel):
    idproducto: int | None
    imagen: str
    nombre: str
    descripcion: str
    categoria: str


