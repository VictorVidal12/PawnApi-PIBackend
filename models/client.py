from pydantic import BaseModel


class Client (BaseModel):
    idCliente: int | None
    nombre: str
    nombre_usuario: str
    correo_electronico: str
    contrasennia: str
    edad: str
    genero: str
