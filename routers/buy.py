from fastapi import APIRouter,status, HTTPException
from db.dbConnector import ConnectionDB
from models.buy import Buy
from fastapi.responses import JSONResponse
from datetime import datetime


dbConnect = ConnectionDB()
buyRouter = APIRouter(prefix="/buy", tags=["buy"])




@buyRouter.get("/{id}", status_code= status.HTTP_200_OK, response_model = list[Buy])
async def get_user_shopping(user_id : int):
    shopping = change_datetime_to_str(dbConnect.get_shopping_by_user_id(user_id))


    return JSONResponse(content=shopping, status_code=status.HTTP_200_OK)
@buyRouter.post("/", status_code= status.HTTP_201_CREATED,response_model=Buy)
async def add_buy(buy: Buy):
    purchase = dbConnect.add_buy(buy.precio, buy.fecha, buy.usuario_idusuario, buy.producto_idproducto, buy.id_factura_compraventa)
    purchase["fecha"] = str(purchase["fecha"])
    if purchase:
        return JSONResponse(content=purchase, status_code=status.HTTP_201_CREATED)


def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        raise  HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post a purchase with this format (YYYY-MM-DD)")

def change_datetime_to_str(lista: list[dict]) -> list[dict]:
    for item in lista:
        item["fecha"] = str(item["fecha"])
    return lista
