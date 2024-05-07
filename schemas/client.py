
def client_schema(client) -> dict:
    return {"idCliente" : str(client[0]),
            "nombre" : str(client[1]),
            "nombre_usuario" : str(client[2]),
            "correo_electronico" : str(client[3]),
            "contrasennia": str(client[4]),
            "edad": str(client[5]),
            "genero": str(client[6])
           }
def clients_schema(clients) -> list:
    return [client_schema(client) for client in clients]

