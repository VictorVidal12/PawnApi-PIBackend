from fastapi import APIRouter,status, HTTPException
from db.dbConnector import ConnectionDB
from models.buy import Buy
from models.sell import Sell
from models.bill_buy_sell import BillBuySell
from fastapi.responses import JSONResponse
from datetime import datetime


dbConnect = ConnectionDB()
buyRouter = APIRouter(prefix="/buy", tags=["buy"])




@buyRouter.get("/{id}", status_code= status.HTTP_200_OK)
async def get_user_purchases(id : int):
    shopping = change_datetime_to_str(dbConnect.get_shopping_by_user_id(id))
    return JSONResponse(content=shopping, status_code=status.HTTP_200_OK)

@buyRouter.post("/shop", status_code= status.HTTP_201_CREATED,response_model=Buy)
async def add_shop_buy_and_client_sell(seller_client_id : int,buy: Buy , bill : BillBuySell):
    idtienda = 8
    if seller_client_id == idtienda:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The buyer client id cannot be the same that the shop (8)")
    bill.total = buy.precio + int(buy.precio * 0.19) + 14500
    bill.precio_IVA = int(buy.precio * 0.19)
    bill.precio_envio = 14500
    bill = add_bill_BillBuySell(bill)
    dbConnect.add_sell(buy.precio, buy.fecha, seller_client_id, buy.producto_idproducto,
                       bill["idFacturaCompra"])
    purchase = dbConnect.add_buy(buy.precio, buy.fecha, idtienda, buy.producto_idproducto,
                                 bill["idFacturaCompra"])
    purchase["fecha"] = str(purchase["fecha"])
    if purchase:
        return JSONResponse(content=purchase, status_code=status.HTTP_201_CREATED)

@buyRouter.post("/client", status_code= status.HTTP_201_CREATED,response_model=Buy)
async def add_client_buy_and_shop_sell(buy: Buy , bill : BillBuySell):
    idtienda = 8
    if buy.usuario_idusuario == idtienda:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The buyer client id cannot be the same that the shop (8)")
    bill.total = buy.precio + int(buy.precio * 0.19) + 14500
    bill.precio_IVA = int(buy.precio * 0.19)
    bill.precio_envio = 14500
    bill = add_bill_BillBuySell(bill)
    dbConnect.add_sell(buy.precio, buy.fecha, idtienda, buy.producto_idproducto,
                       bill["idFacturaCompra"])
    purchase = dbConnect.add_buy(buy.precio, buy.fecha, buy.usuario_idusuario, buy.producto_idproducto,
                                 bill["idFacturaCompra"])
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

def add_sell(sell: Sell):
    sale = dbConnect.add_sell(sell.precio, sell.fecha, sell.usuario_idusuario, sell.producto_idproducto, sell.id_factura_compraventa)
    sale["fecha"] = str(sale["fecha"])
    if sale:
        return JSONResponse(content=sale, status_code=status.HTTP_201_CREATED)


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

def add_bill_BillBuySell(bill: BillBuySell):
    dict_bill = bill.dict()
    dict_bill["municipio"] = dict_bill["municipio"].lower()
    dict_bill["medio_pago"] = check_payment_method(dict_bill["medio_pago"])
    dict_bill["departamento"] = check_department(dict_bill["departamento"])
    if dict_bill["telefono"].isdigit() and len(dict_bill["telefono"]) == 10:
        pass
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number is not valid")
    del dict_bill["idFacturaCompra"]
    bill = dbConnect.add_bill_buy_sell(**dict_bill)
    if bill:
        return bill
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot create the buy-sell  bill" )
