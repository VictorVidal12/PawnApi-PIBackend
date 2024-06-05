from db import dbConnector as dbc


mydb = dbc.ConnectionDB()

if __name__ == "__main__":
    userid = 1
    list_pendings = mydb.get_pending_pawn_offerts_by_userid(userid)
    print(list_pendings)
