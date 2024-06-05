def sell_schema(buy) -> dict:
    return {"idventa": int(buy[0]),
            "precio": int(buy[1]),
            "fecha": str(buy[2]),
            "usuario_idusuario": int(buy[4]),
            "producto_idproducto": int(buy[5])
            }


def sells_schema(sells) -> list:
    return [sell_schema(sell) for sell in sells]
