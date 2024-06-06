from fastapi import APIRouter,status, HTTPException
from db.dbConnector import ConnectionDB
from models.buy import Buy
from fastapi.responses import JSONResponse
import os





IMAGEDIR = "../static/images/"
current_dir = os.path.dirname(os.path.realpath(__file__))
absolute_imagedir = os.path.join(current_dir, IMAGEDIR)

dbConnect = ConnectionDB()
buyRouter = APIRouter(prefix="/buy", tags=["buy"])


@buyRouter.get("/{id}", status_code= status.HTTP_200_OK, response_model = list[Buy])
async def get_buy(idbuy : int):
    shopping = dbConnect.get_shopping_by_user_id(idbuy)
    return JSONResponse(content=shopping, status_code=status.HTTP_200_OK)