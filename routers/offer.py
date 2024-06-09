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
    dbConnect.get_user_by_id(id_usuario)
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
        "ofertante" : id_usuario
    }
    offer =dbConnect.add_offer_type_pawn_by_client(offer["precio"], offer["producto_idproducto"], offer["ofertante"])
    return JSONResponse(content=offer, status_code=status.HTTP_201_CREATED)

@offerRouter.post("/MakeSellByClient", status_code= status.HTTP_201_CREATED, response_model=Offer)
async def offer(nombre, descripcion, categoria, precio : int, id_usuario: int,image: UploadFile = File(...)):
    dbConnect.get_user_by_id(id_usuario)
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
    offer = {
        "precio" : precio,
        "producto_idproducto" : product["idproducto"],
        "ofertante" : id_usuario
    }
    offer =dbConnect.add_offer_type_sell_by_client(offer["precio"], offer["producto_idproducto"], offer["ofertante"])
    return JSONResponse(content=offer, status_code=status.HTTP_201_CREATED)
@offerRouter.get("/SalesByShop", status_code=status.HTTP_200_OK)
async def salesByShop():
    sales = dbConnect.get_products_selling_by_shop()
    return JSONResponse(content=sales, status_code=status.HTTP_200_OK)
def delete_image(image_path: str):
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")

@offerRouter.get("/getAllPendingPawns")
async def get_all_pending_pawns():
    offers = dbConnect.get_pawns_offers_by_shop_in_peding_state()
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)

@offerRouter.get("/pending_pawn_offers_not_finalized_by_userid/{idusuario}", status_code=status.HTTP_200_OK)
async def get_pending_offers_not_finalized_by_userid(idusuario: int):
    offers = dbConnect.get_all_pawn_peding_offers_without_finalized_by_userid(idusuario)
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)


@offerRouter.get("/pending_sell_offers_not_finalized_by_userid/{idusuario}", status_code=status.HTTP_200_OK)
async def get_pending_offers_not_finalized_by_userid(idusuario: int):
    offers = dbConnect.get_all_sell_peding_offers_without_finalized_by_userid(idusuario)
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)

@offerRouter.get("/on_the_way_offer_pawns")
async def on_the_way_offer_pawns():
    offers = dbConnect.get_all_pawn_on_the_way_offers()
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)

@offerRouter.get("/on_the_way_offer_sells")
async def on_the_way_offer_pawns():
    offers = dbConnect.get_all_sell_offers_on_the_way()
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)


@offerRouter.get("/sell_offers_not_finalized")
async def sell_offers_not_finalized():
    offers = dbConnect.get_all_sell_peding_offers_without_finalized_state()
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)




@offerRouter.get("/pawn_offers_not_finalized")
async def pawn_offers_not_finalized():
    offers = dbConnect.get_all_pawn_peding_offers_without_finalized_state()
    return JSONResponse(content=offers, status_code=status.HTTP_200_OK)





@offerRouter.put("/update_offer_state", status_code=status.HTTP_200_OK, response_model=Offer)
async def update_offer_state(id:int, state:str):
    state = check_state(state)
    offer = dbConnect.update_offer_state(id, state)
    return JSONResponse(content=offer, status_code=status.HTTP_200_OK)


def check_category(categoria: str):
    categorias = ["electrónica", "moda", "hogar","salud","entretenimiento","deportes", "transporte", "mascotas","arte", "literatura"]
    if categoria.lower() in categorias:
        return categoria.lower()
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an product with those categories (electrónica ,moda, hogar,salud,entretenimiento,deportes, transporte, mascotas,arte, literatura)")
def check_state(estado : str):
    estados = ["pendiente_cliente","pendiente_tienda","rechazada","en_curso", "finalizada"]
    if estado.lower() in estados:
        return estado.lower()
    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You can only post an product with those states (pendiente_cliente,pendiente_tienda,rechazada,en_curso, finalizada)")