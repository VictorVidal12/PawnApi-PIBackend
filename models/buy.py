from pydantic import BaseModel


class Buy(BaseModel):
    idcompra: int | None
    precio: int
    fecha: str
    medio_pago: str
    usuario_idusuario: int
    producto_idproducto: int
