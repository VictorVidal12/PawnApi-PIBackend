from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    id = 1
    list = mydb.get_peding_sell_offer_by_userid(4)
    print(list)
