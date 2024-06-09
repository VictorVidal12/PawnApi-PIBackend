from fastapi import APIRouter,status, HTTPException
from db.dbConnector import ConnectionDB
from models.sell import Sell
from fastapi.responses import JSONResponse
from datetime import datetime


dbConnect = ConnectionDB()
sellRouter = APIRouter(prefix="/sell", tags=["sell"])




@sellRouter.get("/{id}", status_code= status.HTTP_200_OK)
async def get_user_shopping(id : int):
    sales = change_datetime_to_str(dbConnect.get_sells_by_userid(id))
    return JSONResponse(content=sales, status_code=status.HTTP_200_OK)


def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        raise  HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post a sale with this format (YYYY-MM-DD)")

def change_datetime_to_str(lista: list[dict]) -> list[dict]:
    for item in lista:
        item["fecha"] = str(item["fecha"])
    return lista
