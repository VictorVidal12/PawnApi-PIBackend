from db import dbConnector as dbc

mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    offers = mydb.update_pawn_state_to_paid_by_client(15, 6)
    print(offers)
