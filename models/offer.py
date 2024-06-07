from pydantic import BaseModel


class Offer(BaseModel):
    idoferta: int | None
    tipo: str
    precio: int
    producto_idproducto : int
    estado: str
    ofertante: int
    aceptante : int | None


