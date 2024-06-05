from fastapi import APIRouter, status, HTTPException, UploadFile, File
from db.dbConnector import ConnectionDB
from models.sell import Sell
from schemas.sell import *
from fastapi.responses import JSONResponse
import os
from tools.upload_image import upload_img

IMAGEDIR = "../static/images/"
current_dir = os.path.dirname(os.path.realpath(__file__))
absolute_imagedir = os.path.join(current_dir, IMAGEDIR)

dbConnect = ConnectionDB()
productRouter = APIRouter(prefix="/sell", tags=["sells"])


@productRouter.get("/", status_code=status.HTTP_200_OK, response_model=Sell)
async def get_sells():
    sells = dbConnect.get_sells()
    sells = sells_schema(sells)
    return JSONResponse(content=sells, status_code=status.HTTP_200_OK)
