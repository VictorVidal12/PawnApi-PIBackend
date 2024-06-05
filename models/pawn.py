from pydantic import BaseModel


class Pawn(BaseModel):
    idempennio: int | None
    precio: int
    estado: str
    fecha_inicio: str
    fecha_final: str
    interes: int
    usuario_idusuario: int
    producto_idproducto: int
