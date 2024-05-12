from pydantic import BaseModel


class User (BaseModel):
    idusuario: int | None
    nombre: str
    correo_electronico: str
    contrasennia: str
    tipo: str

