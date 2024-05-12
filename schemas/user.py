
def user_schema(user) -> dict:
    return {"idusuario" : int(user[0]),
            "nombre" : str(user[1]),
            "correo_electronico" : str(user[2]),
            "contrasennia": str(user[3]),
            "tipo": str(user[4])
           }
def users_schema(users) -> list:
    return [user_schema(user) for user in users]

