from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":

    list = mydb.get_sells_by_userid(8)
    print(list)
