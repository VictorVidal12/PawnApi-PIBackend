from fastapi import APIRouter, status, HTTPException
from db.dbConnector import ConnectionDB
from models.client import Client
from schemas.client import *
from fastapi.responses import JSONResponse

dbConnect = ConnectionDB()
clientRouter = APIRouter(prefix="/client", tags=["client"])

@clientRouter.get("/{email}/{password}", status_code= status.HTTP_200_OK, response_model=Client)
async def login_client(email: str , password: str ):
    client = dbConnect.get_client_by_email(email)
    client_dict = client_schema(client)
    if client_dict["correo_electronico"] ==  email and client_dict["contrasennia"] == password:
        return JSONResponse(content=client_dict)
    elif client_dict["correo_electronico"] ==  email and client_dict["contrasennia"] != password:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Incorrect password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Client does not found")


@clientRouter.post("/", status_code= status.HTTP_201_CREATED, response_model=Client)
async def client(client: Client):
    client_dict = dict(client)
    client_dict["genero"] = correctGenre(client_dict["genero"])
    del client_dict["idCliente"]
    dbConnect.add_client(**client_dict)
    client_dict = client_schema(dbConnect.get_client_by_email(client.correo_electronico))
    return JSONResponse(content=client_dict)
def correctGenre(word: str):
    word_lower = word.lower()
    if word_lower == "masculino" or word_lower == "femenino" or word_lower == "otro":
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post an owner with those genres(masculino,femenino or otro)")