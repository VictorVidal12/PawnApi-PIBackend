from fastapi import APIRouter, status, HTTPException, UploadFile, File
from db.dbConnector import ConnectionDB
from models.product import Product
from schemas.product import *
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
    product_dict = product_schema(product)
    return JSONResponse(content=product_dict, status_code=status.HTTP_200_OK)

@productRouter.post("/", status_code= status.HTTP_201_CREATED)
async def product(nombre, descripcion, categoria, image: UploadFile = File(...)):
    categoria = check_category(categoria)
    img_dir = await upload_img(absolute_imagedir, image)
    dict_product = {
        "imagen" : str(img_dir),
        "nombre" : nombre,
        "descripcion" : descripcion,
        "categoria" : categoria
    }
    dbConnect.add_product(dict_product["imagen"],dict_product["nombre"], dict_product["descripcion"], dict_product["categoria"] )
    product = dbConnect.get_product_by_image(img_dir)
    return JSONResponse(content=product_schema(product), status_code=status.HTTP_201_CREATED)

@productRouter.put("/", status_code= status.HTTP_200_OK, response_model = Product)
async def product_strings(product: Product):
    product.categoria = check_category(product.categoria)
    dict_product =  dict(product)
    dbConnect.update_product(dict_product["idproducto"], dict_product["nombre"], dict_product["descripcion"], dict_product["categoria"])
    product_dict = product_schema(dbConnect.get_product_by_id(dict_product["idproducto"]))
    return JSONResponse(content=product_dict, status_code=status.HTTP_200_OK)

@productRouter.put("/{id}", status_code= status.HTTP_200_OK, response_model = Product)
async def img_product(id :str ,image: UploadFile):
    product = product_schema(dbConnect.get_product_by_id(int(id)))
    image_path = absolute_imagedir+product["imagen"]
    delete_image(image_path)
    img_dir = await upload_img(absolute_imagedir, image)
    dbConnect.update_product_image(int(id), img_dir)
    product = dbConnect.get_product_by_id(int(id))
    return JSONResponse(content=product_schema(product), status_code=status.HTTP_200_OK)

@productRouter.delete("/{id}", status_code= status.HTTP_200_OK)
async def product(idproducto : str):
    product = product_schema(dbConnect.get_product_by_id(int(idproducto)))
    dbConnect.delete_product(product["idproducto"])
    delete_image(absolute_imagedir+product["imagen"])
    return JSONResponse(content={"message": "Product deleted"}, status_code=status.HTTP_200_OK)
def delete_image(image_path: str):
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")





def check_category(categoria: str):
    categorias = ["electrónica", ",moda", "hogar","salud","entretenimiento","deportes", "transporte", "mascotas","arte", "literatura"]
    if categoria.lower() in categorias:
        return categoria.lower().capitalize()
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an product with those categories (electrónica ,moda, hogar,salud,entretenimiento,deportes, transporte, mascotas,arte, literatura)")