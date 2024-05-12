def product_schema(product) -> dict:
    return {"idproducto" : int(product[0]),
            "imagen" : str(product[1]),
            "nombre" : str(product[2]),
            "descripcion": str(product[3]),
            "categoria": str(product[4])
           }
def products_schema(products) -> list:
    return [product_schema(product) for product in products]

