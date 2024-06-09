from fastapi import APIRouter, status, HTTPException
from db.dbConnector import ConnectionDB
from models.bill_buy_sell import BillBuySell
from models.bill_pawn import BillPawn
from models.bill_pawn_pay import BillPayPawn
from fastapi.responses import JSONResponse
from datetime import datetime

dbConnect = ConnectionDB()
billRouter = APIRouter(prefix="/bill", tags=["bill"])


@billRouter.post("/BillBuySell", status_code=status.HTTP_201_CREATED, response_model=BillBuySell)
async def add_bill_BillBuySell(bill: BillBuySell):
    dict_bill = bill.dict()
    dict_bill["municipio"] = dict_bill["municipio"].lower().capitalize()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number is not valid")
    del dict_bill["idFacturaCompra"]
    bill = dbConnect.add_bill_buy_sell(**dict_bill)
    if bill:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=bill)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the buy-sell  bill" )

@billRouter.post("/BillPawn", status_code=status.HTTP_201_CREATED, response_model=BillPawn)
async def add_bill_BillPawn(bill: BillPawn):
    dict_bill = bill.dict()
    dict_bill["municipio"] = dict_bill["municipio"].lower().capitalize()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Phone is invalid")
    del dict_bill["idFacturaEmpennio"]
    bill = dbConnect.add_bill_pawn(**dict_bill)
    if bill:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=bill)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the pawn bill" )



@billRouter.post("/BillPayPawn", status_code=status.HTTP_201_CREATED, response_model=BillPayPawn)
async def add_bill_BillPayPawn(bill: BillPayPawn):
    dict_bill = bill.dict()
    dict_bill["municipio"] = dict_bill["municipio"].lower().capitalize()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Phone is invalid")
    del dict_bill["idFacturaEmpennio"]
    bill = dbConnect.add_bill_pay_pawn(**dict_bill)
    if bill:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=bill)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the pawn payment bill" )


def check_payment_method(medio_pago: str) -> str:
    methods = ["pse", "tarjeta_debito","tarjeta_credito", "transferencia", "efectivo"]
    if medio_pago.lower() in methods:
        return medio_pago.lower().capitalize()
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
        return departamento.lower().capitalize()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The departament is incorrect")
