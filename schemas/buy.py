def buy_schema(buy) -> dict:
    return {"idcompra": int(buy[0]),
            "precio": int(buy[1]),
            "fecha": str(buy[2]),
            "medio_pago": str(buy[3]),
            "usuario_idusuario": int(buy[4]),
            "producto_idproducto": int(buy[5])
            }


def buys_schema(buys) -> list:
    return [buy_schema(buy) for buy in buys]
