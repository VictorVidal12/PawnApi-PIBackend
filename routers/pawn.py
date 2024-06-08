from fastapi import APIRouter,status, HTTPException
from datetime import datetime
from db.dbConnector import ConnectionDB
from models.pawn import Pawn
from fastapi.responses import JSONResponse

dbConnect = ConnectionDB()
pawnRouter = APIRouter(prefix="/pawn", tags=["pawn"])

@pawnRouter.get("/currentShop", status_code= status.HTTP_200_OK, response_model = list[Pawn])
async def get_user_shopping():
    pawns = change_datetime_to_str(dbConnect.get_currents_pawns_by_shop())
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)



@pawnRouter.post("/",)

















def check_date(date: str) -> bool:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        raise  HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You can only post a sale with this format (YYYY-MM-DD)")

def change_datetime_to_str(lista: list[dict]) -> list[dict]:
    for item in lista:
        item["fecha_inicio"] = str(item["fecha_inicio"])
        item["fecha_final"] = str(item["fecha_final"])
    return lista


#en_curso , vencido y pagado