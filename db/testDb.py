from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    offers = mydb.get_products_selling_by_shop()
    print(offers)
