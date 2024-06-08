from pydantic import BaseModel


class Sell(BaseModel):
    idventa: int | None
    precio: int
    fecha: str
    usuario_idusuario: int
    producto_idproducto: int
    id_factura_compraventa : int

