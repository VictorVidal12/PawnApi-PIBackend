from fastapi import APIRouter, status, HTTPException, UploadFile, File
from db.dbConnector import ConnectionDB
from models.offer import Offer
from fastapi.responses import JSONResponse
import os
from tools.upload_image import upload_img


IMAGEDIR = "../static/images/"
current_dir = os.path.dirname(os.path.realpath(__file__))
absolute_imagedir = os.path.join(current_dir, IMAGEDIR)

dbConnect = ConnectionDB()
offerRouter = APIRouter(prefix="/offer", tags=["offer"])

@offerRouter.post("/MakePawnByClient", status_code= status.HTTP_201_CREATED,response_model=Offer)
async def offer(nombre, descripcion, categoria, precio : int, id_usuario : int,image: UploadFile = File(...)):
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
    dbConnect.get_user_by_id(id_usuario)
    offer = {
        "precio" : precio,
        "producto_idproducto" : product["idproducto"],
        "usuario_idusuario" : id_usuario
    }
    offer =dbConnect.add_offer_type_pawn_by_client(offer["precio"], offer["producto_idproducto"], offer["usuario_idusuario"])
    return JSONResponse(content=offer, status_code=status.HTTP_201_CREATED)

@offerRouter.post("/MakeSellByClient", status_code= status.HTTP_201_CREATED, response_model=Offer)
async def offer(nombre, descripcion, categoria, precio : int, usuario_idusario : int,image: UploadFile = File(...)):
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
    dbConnect.get_user_by_id(usuario_idusario)
    offer = {
        "precio" : precio,
        "producto_idproducto" : product["idproducto"],
        "usuario_idusuario" : usuario_idusario
    }
    offer =dbConnect.add_offer_type_sell_by_client(offer["precio"], offer["producto_idproducto"], offer["usuario_idusuario"])
    return JSONResponse(content=offer, status_code=status.HTTP_201_CREATED)

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
def check_state(estado : str):
    estados = ["pendiente_cliente","pendiente_tienda","rechazada","en_curso", "finalizada"]
    if estado.lower() in estados:
        return estado.lower().capitalize()
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an product with those states (pendiente_cliente,pendiente_tienda,rechazada,en_curso, finalizada)")