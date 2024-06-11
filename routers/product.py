from fastapi import APIRouter, status, HTTPException, UploadFile, File
from db.dbConnector import ConnectionDB
from models.product import Product
from fastapi.responses import JSONResponse
import os
from tools.upload_image import upload_img

IMAGEDIR = "../static/images/"
current_dir = os.path.dirname(os.path.realpath(__file__))
absolute_imagedir = os.path.join(current_dir, IMAGEDIR)

dbConnect = ConnectionDB()
productRouter = APIRouter(prefix="/product", tags=["product"])

@productRouter.get("/{id}", status_code= status.HTTP_200_OK, response_model = Product)
async def get_product(idproducto : str):
    product = dbConnect.get_product_by_id(int(idproducto))
    product_dict = product
    return JSONResponse(content=product_dict, status_code=status.HTTP_200_OK)

@productRouter.put("/", status_code= status.HTTP_200_OK, response_model = Product)
async def product_strings(id :int,nombre :str, descripcion :str, categoria :str):
    categoria = check_category(categoria)
    dbConnect.update_product(id, nombre, descripcion, categoria)
    product_dict = dbConnect.get_product_by_id(id)
    return JSONResponse(content=product_dict, status_code=status.HTTP_200_OK)

@productRouter.put("/{id}", status_code= status.HTTP_200_OK, response_model = Product)
async def img_product(id :str ,image: UploadFile = File(...)):
    product = dbConnect.get_product_by_id(int(id))
    image_path = absolute_imagedir+product["imagen"]
    delete_image(image_path)
    img_dir = await upload_img(absolute_imagedir, image)
    dbConnect.update_product_image(int(id), img_dir)
    product = dbConnect.get_product_by_id(int(id))
    return JSONResponse(content=product, status_code=status.HTTP_200_OK)

@productRouter.put("/image/{id}", status_code= status.HTTP_201_CREATED)
async def add_image_to_product(id : int, image: UploadFile = File(...)):
    img_dir = await upload_img(absolute_imagedir, image)
    dbConnect.update_product_image(int(id), img_dir)
    product = dbConnect.get_product_by_id(int(id))
    return JSONResponse(content=product, status_code=status.HTTP_200_OK)



def delete_image(image_path: str):
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")





def check_category(categoria: str):
    categorias = ["electrónica", "moda", "hogar","salud","entretenimiento","deportes", "transporte", "mascotas","arte", "literatura"]
    if categoria.lower() in categorias:
        return categoria.lower().capitalize()
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an product with those categories (electrónica ,moda, hogar,salud,entretenimiento,deportes, transporte, mascotas,arte, literatura)")