from pydantic import BaseModel


class Offer(BaseModel):
    idOferta: int | None
    tipo: str
    precio: int
    producto_idproducto : int
    estado: str
    usuario_idusuario: int
