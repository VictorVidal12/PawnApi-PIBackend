from fastapi import APIRouter,status, HTTPException
from datetime import datetime
from db.dbConnector import ConnectionDB
from models.pawn import Pawn
from fastapi.responses import JSONResponse

dbConnect = ConnectionDB()
pawnRouter = APIRouter(prefix="/pawn", tags=["pawn"])

@pawnRouter.get("/currentShop", status_code= status.HTTP_200_OK)
async def get_shop_pawns():
    pawns = change_datetime_to_str(dbConnect.get_currents_pawns_by_shop())
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)

@pawnRouter.get("/clientPawns/{id}", status_code= status.HTTP_200_OK)
async def get_client_pawns(id: int):
    pawns = change_datetime_to_str(dbConnect.get_currents_pawns_by_userid(id))
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)

@pawnRouter.post("/addPawn", status_code= status.HTTP_201_CREATED, response_model = Pawn)
async def add_pawn(pawn: Pawn):
    pawn = change_item_datetime_to_str(dbConnect.add_pawn(pawn.precio, pawn.fecha_inicio, pawn.fecha_final, pawn.usuario_idusuario, pawn.producto_idproducto, pawn.id_factura_empennio))
    return JSONResponse(content=pawn, status_code=status.HTTP_201_CREATED)



@pawnRouter.put("/payPawn/{id}", status_code= status.HTTP_200_OK, response_model = Pawn)
async def pay_pawn(id: int, id_factura_pago_cliente_empennio: int):
    pawn = change_item_datetime_to_str(dbConnect.pay_pawn(id,id_factura_pago_cliente_empennio))
    return JSONResponse(content=pawn, status_code=status.HTTP_200_OK)



















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

def change_item_datetime_to_str(item: dict) -> dict:
    item["fecha_inicio"] = str(item["fecha_inicio"])
    item["fecha_final"] = str(item["fecha_final"])
    return item

#en_curso , vencido y pagado