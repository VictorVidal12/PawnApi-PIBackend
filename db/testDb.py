from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    lista = mydb.get_users()
    print(lista)
