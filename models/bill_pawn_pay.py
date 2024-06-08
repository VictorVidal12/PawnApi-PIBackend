from pydantic import BaseModel

class BillPayPawn(BaseModel):
    idFacturaEmpennio: int | None
    medio_pago :str
    total : int
    nombres : str
    apellidos : str
    direccion :str
    departamento : str
    municipio:str
    telefono : str
    correo : str
    precio_envio : int
    precio_IVA : int
    info_adicional : str