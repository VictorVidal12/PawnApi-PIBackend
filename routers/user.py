from fastapi import APIRouter, status, HTTPException
from db.dbConnector import ConnectionDB
from models.user import User
from fastapi.responses import JSONResponse
from tools.token import create_jwt_token
from datetime import datetime
dbConnect = ConnectionDB()
userRouter = APIRouter(prefix="/user", tags=["user"])

@userRouter.post("/login", status_code= status.HTTP_200_OK)
async def login_user(email: str , password: str ):
    user = dbConnect.get_user_by_email(email)
    user["nacimiento"] = str(user["nacimiento"])
    user_dict = user
    if user_dict["correo_electronico"] ==  email and user_dict["contrasennia"] == password:
        user_dict_token ={"data" : user_dict, "token" : create_jwt_token(user_dict)}
        return JSONResponse(content= user_dict_token)
    elif user_dict["correo_electronico"] ==  email and user_dict["contrasennia"] != password:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Incorrect password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "user does not found")


@userRouter.post("/", status_code= status.HTTP_201_CREATED, response_model=User)
async def user(user: User):
    user.tipo = correctType(user.tipo)
    user.genero = correctGenre(correctGenre(user.genero))
    check_date(user.nacimiento)
    user_dict = dict(user)
    del user_dict["idusuario"]
    dbConnect.add_user(**user_dict)
    user_dict = dbConnect.get_user_by_email(user.correo_electronico)
    user_dict["nacimiento"] = str(user_dict["nacimiento"])
    print(user_dict)
    return JSONResponse(content=user_dict)

@userRouter.delete("/{email}", status_code= status.HTTP_200_OK)
async def user(email : str):
    user = dbConnect.get_user_by_email(email)
    user_dict = user
    dbConnect.delete_user(email)
    return JSONResponse(content=user_dict)
@userRouter.put("/",status_code= status.HTTP_200_OK, response_model=User)
async def user(user: User):
    user.tipo = correctType(user.tipo)
    user_dict = dict(user)
    del user_dict["idusuario"]
    dbConnect.update_user(user.correo_electronico, user_dict["nombre"], user_dict["contrasennia"], user_dict["tipo"])
    user_dict = dbConnect.get_user_by_email(user.correo_electronico)
    return JSONResponse(content=user_dict)
def correctType(word: str):
    word_lower = word.lower()
    if word_lower == "administrador" or word_lower == "cliente" :
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post an user with those types (administrador, cliente)")

def correctGenre(word :str):
    word_lower = word.lower()
    if word_lower == "femenino" or word_lower == "masculino" or "otro":
        return word_lower
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an user with those genres (masculino,femenino u otro)")

def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        raise  HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post an user with this format (YYYY-MM-DD)")