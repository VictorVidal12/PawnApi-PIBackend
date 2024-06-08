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
    id_factura_empennio: int
    id_factura_pago_cliente_empennio : int | None
