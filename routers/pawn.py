from fastapi import APIRouter,status, HTTPException
from datetime import datetime
from db.dbConnector import ConnectionDB
from models.pawn import Pawn
from models.bill_pawn_pay import BillPayPawn
from models.bill_pawn import  BillPawn
from fastapi.responses import JSONResponse

dbConnect = ConnectionDB()
pawnRouter = APIRouter(prefix="/pawn", tags=["pawn"])

@pawnRouter.get("/currentShop", status_code= status.HTTP_200_OK)
async def get_shop_pawns():
    pawns = change_datetime_to_str(dbConnect.get_currents_pawns_by_shop())
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)

@pawnRouter.get("/clientCurrentPawns/{id}", status_code= status.HTTP_200_OK)
async def get_client_current_pawns(id: int):
    pawns = change_datetime_to_str(dbConnect.get_currents_pawns_by_userid(id))
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)

@pawnRouter.get("/clientPawns/{id}", status_code= status.HTTP_200_OK)
async def get_user_pawns(id: int):
    pawns = change_datetime_to_str(dbConnect.get_pawns_by_userid(id))
    return JSONResponse(content=pawns, status_code=status.HTTP_200_OK)
@pawnRouter.post("/addPawn", status_code= status.HTTP_201_CREATED, response_model = Pawn)
async def add_pawn(pawn: Pawn):
    billDict2 =  {
        "idFacturaEmpennio": 9,
        "medio_pago": "pse",
        "total": pawn.precio + int(pawn.precio * 0.05) + int(pawn.precio * 0.19) +14500,
        "nombres": "PAWNS",
        "apellidos": "COMPANY",
        "direccion": "Carrera 70 #43-122 ",
        "departamento": "Antioquia",
        "municipio": "Medellin",
        "telefono": "3007900564",
        "correo": "correo@gmail.com",
        "precio_envio":  14500,
        "precio_IVA": int(pawn.precio * 0.19),
        "info_adicional": "pago de empennio a cliente ejemplo"
    }
    billPawn = add_bill_BillPawn(billDict2)
    pawn = change_item_datetime_to_str(dbConnect.add_pawn(pawn.precio, pawn.fecha_inicio, pawn.fecha_final, pawn.usuario_idusuario, pawn.producto_idproducto, billPawn["idFacturaEmpennio"]))
    return JSONResponse(content=pawn, status_code=status.HTTP_201_CREATED)



@pawnRouter.put("/payPawn/{id}", status_code= status.HTTP_200_OK, response_model = Pawn)
async def pay_pawn(id: int, bill : BillPayPawn):
    pawn = dbConnect.get_pawn_by_id(id)
    bill.total = pawn["precio"] + int(pawn["precio"] * 0.05) + int(pawn["precio"] * 0.19) +14500
    bill.precio_IVA = int(pawn["precio"] * 0.19)
    bill.precio_envio = 14500
    bill_bd = add_bill_BillPayPawn(bill)
    pawn = change_item_datetime_to_str(dbConnect.pay_pawn(id, bill_bd["idFacturaEmpennio"]))
    return JSONResponse(content=pawn, status_code=status.HTTP_200_OK)



def add_bill_BillPayPawn(bill: BillPayPawn):
    dict_bill = bill.dict()
    dict_bill["municipio"] = dict_bill["municipio"].lower()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Phone is invalid")
    del dict_bill["idFacturaEmpennio"]
    bill = dbConnect.add_bill_pay_pawn(**dict_bill)
    if bill:
        return bill
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the pawn payment bill" )


def add_bill_BillPawn(bill:dict):
    dict_bill = bill
    dict_bill["municipio"] = dict_bill["municipio"].lower()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Phone is invalid")
    del dict_bill["idFacturaEmpennio"]
    bill = dbConnect.add_bill_pawn(**dict_bill)
    if bill:
        return bill
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the pawn bill" )















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


def check_payment_method(medio_pago: str) -> str:
    methods = ["pse", "tarjeta_debito","tarjeta_credito", "transferencia", "efectivo"]
    if medio_pago.lower() in methods:
        return medio_pago.lower()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The payment method is incorrect")


def check_department(departamento: str) -> str:
    departamentos_colombia = [
        "amazonas",
        "antioquia",
        "arauca",
        "atlantico",
        "bolivar",
        "boyaca",
        "caldas",
        "caqueta",
        "casanare",
        "cauca",
        "cesar",
        "choco",
        "cordoba",
        "cundinamarca",
        "guainia",
        "guaviare",
        "huila",
        "la_guajira",
        "magdalena",
        "meta",
        "narino",
        "norte_de_santander",
        "putumayo",
        "quindio",
        "risaralda",
        "san_andres_y_providencia",
        "santander",
        "sucre",
        "tolima",
        "valle_del_cauca",
        "vaupes",
        "vichada"
    ]
    if departamento.lower() in departamentos_colombia:
        return departamento.lower()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The departament is incorrect")
