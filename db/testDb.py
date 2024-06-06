from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    id = 1
    list = mydb.get_pending_sell_offerts_by_userid(1)
    print(list)
