from fastapi import HTTPException, status
from mysql.connector import pooling
from datetime import datetime


class ConnectionDB:

    def __init__(self):
        dbconfig = {'user': 'myadmin',
                    'host': 'serverflexibletest.mysql.database.azure.com',
                    'password': 'HolaMundo*',
                    'database': 'mydb',
                    'port': 3306,  # Puerto predeterminado de MySQL
                    'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias
        self.conn = None  # Mantén la conexión abierta en la instancia
        self.pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                                pool_size=5,
                                                **dbconfig)

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        connection = self.pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            # Agregar la propiedad y obtener el id de la propiedad recién agregada
            cursor.execute(consulta_sql, variables_adicionales)

            if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                    "UPDATE") or consulta_sql.strip().upper().startswith(
                "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                connection.commit()

                return cursor.lastrowid if consulta_sql.strip().upper().startswith("INSERT") else None
            result = cursor.fetchall()

            return result
        except Exception as e:
            raise e
        finally:
            cursor.close()
            connection.close()

    # USUARIOS
    def exists_shop_type_user_with_this_id(self, idusuario):
        query = "SELECT * FROM usuario WHERE tipo = 'tienda' AND idusuario = %s;"
        shop_users = self.executeSQL(query, (idusuario,))
        if len(shop_users) > 0:
            return True
        else:
            return False

    def exists_client_type_user_with_this_id(self, idusuario):
        query = "SELECT * FROM usuario WHERE tipo = 'cliente' AND idusuario = %s;"
        shop_users = self.executeSQL(query, (idusuario,))
        if len(shop_users) > 0:
            return True
        else:
            return False

    def get_users(self):
        query = "SELECT * FROM USUARIO"
        users = self.executeSQL(query)
        return users

    def get_user_by_email(self, email):
        query = "SELECT * FROM USUARIO u WHERE u.correo_electronico = %s;"
        user = self.executeSQL(query, (email,))
        if len(user) > 0:
            return user[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email was not found")

    def get_user_by_id(self, idusuario: int):
        query = "SELECT * FROM USUARIO u WHERE u.idusuario = %s;"
        user = self.executeSQL(query, (idusuario,))
        if len(user) > 0:
            return user[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    def add_user(self, nombre: str, correo_electronico: str, contrasennia: str, tipo: str
                 , genero: str, nacimiento: str, telefono: str):
        if self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post an User with an existing email")
        else:
            query = "INSERT INTO `mydb`.`USUARIO` (`nombre`,`correo_electronico`,`contrasennia`,`tipo`, `genero`,`nacimiento`,`telefono`) " \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s);"
            variables = (nombre, correo_electronico, contrasennia, tipo, genero, nacimiento, telefono)
            self.executeSQL(query, variables)
            query_2 = "SELECT * FROM usuario ORDER BY idusuario DESC LIMIT 1;"
            element = self.executeSQL(query_2)
            return element

    def delete_user(self, correo_electronico: str):
        if not self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with this email does not exist")
        else:
            query = "DELETE FROM `mydb`.`USUARIO` WHERE `correo_electronico` = %s;"
            variables = (correo_electronico,)
            self.executeSQL(query, variables)

    def update_user(self, correo_electronico: str, nuevo_nombre: str, nueva_contrasennia: str, nuevo_tipo: str,
                    nuevo_genero: str, nuevo_nacimiento: str, nuevo_telefono: str):
        if not self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with this email does not exist")
        else:
            query = "UPDATE `mydb`.`USUARIO` SET `nombre` = %s, `contrasennia` = %s, `tipo` = %s, `genero` = %s, " \
                    "`nacimiento` = %s, `telefono` = %s WHERE `correo_electronico` = %s;"
            variables = (nuevo_genero, nuevo_nacimiento, nuevo_telefono, nuevo_nombre, nueva_contrasennia, nuevo_tipo,
                         correo_electronico)
            self.executeSQL(query, variables)

    def user_with_this_email_exist(self, correo):
        query = "SELECT * FROM USUARIO u WHERE u.correo_electronico = %s;"
        user = self.executeSQL(query, (correo,))
        if len(user) > 0:
            return True
        else:
            return False

    # PRODUCTO
    def get_product_by_id(self, idproducto: int):
        query = "SELECT * FROM PRODUCTO p WHERE p.idproducto = %s;"
        product = self.executeSQL(query, (idproducto,))
        if len(product) > 0:
            return product[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")

    def add_product(self, imagen: str, nombre: str, descripcion: str, categoria: str):
        query = "INSERT INTO `mydb`.`PRODUCTO` (`imagen`,`nombre`,`descripcion`,`categoria`) " \
                "VALUES (%s,%s,%s,%s);"
        variables = (imagen, nombre, descripcion, categoria)
        self.executeSQL(query, variables)
        query_2 = "SELECT * FROM producto ORDER BY idproducto DESC LIMIT 1;"
        element = self.executeSQL(query_2)
        return element

    def get_product_by_image(self, image: str):
        query = "SELECT * FROM PRODUCTO p WHERE p.imagen = %s;"
        product = self.executeSQL(query, (image,))
        if len(product) > 0:
            return product[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this image was not found")

    def delete_product(self, idproducto: int):
        if not self.product_with_this_id_exist(idproducto):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product with this id does not exist")
        else:
            query = "DELETE FROM `mydb`.`PRODUCTO` WHERE `idproducto` = %s;"
            variables = (idproducto,)
            self.executeSQL(query, variables)

    def update_product(self, idproducto: int, nuevo_nombre: str, nueva_descripcion: str, nueva_categoria: str):
        if not self.product_with_this_id_exist(idproducto):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product with this id does not exist")
        else:
            query = "UPDATE `mydb`.`PRODUCTO` SET  `nombre` = %s, `descripcion` = %s, `categoria` = %s " \
                    "WHERE `idproducto` = %s;"
            variables = (nuevo_nombre, nueva_descripcion, nueva_categoria, idproducto,)
            self.executeSQL(query, variables)

    def update_product_image(self, idproducto: int, imagen: str):
        if not self.product_with_this_id_exist(idproducto):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product with this id does not exist")
        else:
            query = "UPDATE `mydb`.`PRODUCTO` SET  `imagen` = %s " \
                    "WHERE `idproducto` = %s;"
            variables = (imagen, idproducto,)
            self.executeSQL(query, variables)

    def product_with_this_id_exist(self, idproducto):
        query = "SELECT * FROM PRODUCTO p WHERE p.idproducto = %s;"
        product = self.executeSQL(query, (idproducto,))
        if len(product) > 0:
            return True
        else:
            return False

    #OFERTA

    def get_peding_client_state_pawns_offers_by_userid(self, userid):
        if self.get_user_by_id(userid):
            query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                    " WHERE o.ofertante = %s AND o.tipo = 'empennio' AND o.estado = 'pendiente_cliente';"

            offers = self.executeSQL(query, (userid,))
            if len(offers) > 0:
                return offers
            else:
                return []

    def get_peding_client_state_sell_offers_by_userid(self, userid):
        if self.get_user_by_id(userid):
            query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                    " WHERE o.ofertante = %s AND o.tipo = 'venta' AND o.estado = 'pendiente_cliente';"
            offers = self.executeSQL(query, (userid,))
            if len(offers) > 0:
                return offers
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Offers with this user id was not found in this offers states")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offers with this user id was not found in pawns type offers")

    def get_peding_shop_state_pawns_offers_by_userid(self, userid):
        if self.get_user_by_id(userid):
            query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                    " WHERE o.ofertante = %s AND o.tipo = 'empennio' AND o.estado = 'pendiente_tienda';"

            offers = self.executeSQL(query, (userid,))
            if len(offers) > 0:
                return offers
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Offers with this user id was not found in this offers states")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offers with this user id was not found in pawns type offers")

    def get_peding_shop_state_sell_offers_by_userid(self, userid):
        if self.get_user_by_id(userid):
            query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                    " WHERE o.ofertante = %s AND o.tipo = 'venta' AND o.estado = 'pendiente_tienda';"
            offers = self.executeSQL(query, (userid,))
            if len(offers) > 0:
                return offers
            else:
                return []
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offers with this user id was not found in pawns type offers")

    def exists_offers_pawn_type_with_userid(self, userid: int):
        query = "SELECT * FROM oferta WHERE ofertante = %s AND tipo = 'empennio';"
        offers = self.executeSQL(query, (userid,))
        if len(offers) > 0:
            return True
        else:
            return False

    # El cliente crea la oferta
    # HU: Crear oferta de empeño(cliente)
    def add_offer_type_pawn_by_client(self, precio: int, producto_idproducto: int, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query_1 = "INSERT INTO `mydb`.`oferta` (tipo, precio, producto_idproducto, estado, ofertante)" \
                          " VALUES ('empennio', %s, %s, 'pendiente_tienda', %s);"
                variables_1 = (precio, producto_idproducto, usuario_idusuario,)
                self.executeSQL(query_1, variables_1)

                query_2 = "SELECT * FROM `mydb`.`oferta` ORDER BY idoferta DESC LIMIT 1;"
                result = self.executeSQL(query_2)

                if result:
                    return result[0]  # Devuelve el primer resultado si existe
                else:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Failed to retrieve the inserted offer")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    # El cliente crea la oferta
    # HU: Crear oferta de venta (cliente)
    def add_offer_type_sell_by_client(self, precio: int, producto_idproducto: int, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query_1 = "INSERT INTO `mydb`.`oferta` (tipo, precio, producto_idproducto, estado, ofertante)" \
                          " VALUES ('venta', %s, %s, 'pendiente_tienda', %s);"
                variables_1 = (precio, producto_idproducto, usuario_idusuario,)
                self.executeSQL(query_1, variables_1)
                query_2 = "SELECT * FROM oferta ORDER BY idoferta DESC LIMIT 1;"
                element = self.executeSQL(query_2)
                return element[0]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    # HU: Actualizar oferta para contraofertar el precio (cliente)
    def update_offer_with_counteroffer_client(self, contra_oferta: int, idoferta: int, ofertante: int,
                                              producto_idproducto: int):
        if self.exists_idoffer(idoferta):
            if self.exists_client_type_user_with_this_id(ofertante):
                if self.exists_idproduct(producto_idproducto):
                    query = "UPDATE `mydb`.`oferta` SET `precio` = %s, estado` = 'pendiente_tienda' " \
                            "WHERE `idoferta` = %s AND `producto_idproducto` = %s AND `ofertante` = %s;"
                    variables = (contra_oferta, idoferta, producto_idproducto, ofertante,)
                    self.executeSQL(query, variables)

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with this id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with this id was not found in client type users")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offer with this id was not found")

    def get_all_pawn_peding_offers_without_finalized_by_userid(self, userid):
        self.get_user_by_id(userid)
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                " WHERE o.tipo = 'empennio' AND o.estado != 'finalizada' AND o.ofertante = %s;"
        offers = self.executeSQL(query, (userid,))
        if len(offers) > 0:
            return offers
        else:
            return []

    def get_all_pawn_peding_offers_without_finalized_state(self):
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                " WHERE o.tipo = 'empennio' AND o.estado != 'finalizada'AND o.ofertante != %s;"
        offers = self.executeSQL(query, (8,))
        if len(offers) > 0:
            return offers
        else:
            return []

    def get_all_sell_peding_offers_without_finalized_state(self):
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                " WHERE o.tipo = 'venta' AND o.estado != 'finalizada' AND o.ofertante != %s;"
        offers = self.executeSQL(query, (8,))
        if len(offers) > 0:
            return offers
        else:
            return []


    def get_all_sell_peding_offers_without_finalized_by_userid(self, userid):
        self.get_user_by_id(userid)
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                " WHERE o.tipo = 'venta' AND o.estado != 'finalizada' AND o.ofertante = %s;"
        offers = self.executeSQL(query, (userid,))
        if len(offers) > 0:
            return offers
        else:
            return []

    # HU: Actualizar oferta para contraofertar el precio (tienda)
    def update_offer_with_counteroffer_shop(self, contra_oferta: int, idoferta: int,
                                            producto_idproducto: int):
        idshop = 8
        if self.exists_idoffer(idoferta):
            if self.exists_shop_type_user_with_this_id(idshop):
                if self.exists_idproduct(producto_idproducto):
                    query = "UPDATE `mydb`.`oferta` SET `precio` = %s, estado` = 'pendiente_cliente' " \
                            "WHERE `idoferta` = %s AND `producto_idproducto` = %s AND `ofertante` = %s;"
                    variables = (contra_oferta, idoferta, producto_idproducto, idshop,)
                    self.executeSQL(query, variables)
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with this id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with this id was not found in shop type users")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offer with this id was not found")

    def get_oferta_by_id(self, idoferta: int):
        if self.exists_idoffer(idoferta):
            query = "SELECT * FROM OFERTA o WHERE o.idoferta = %s;"
            oferta = self.executeSQL(query, (idoferta,))
            return oferta[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer with this id was not found")

    def exists_idproduct(self, idproducto: int) -> bool:
        query = "SELECT * FROM producto WHERE idproducto = %s;"
        variables = (idproducto,)
        products_with_id = self.executeSQL(query, variables)
        if len(products_with_id) > 0:
            return True
        else:
            return False

    def exists_iduser(self, idusuario: int) -> bool:
        query = "SELECT * FROM usuario WHERE idusuario = %s;"
        variables = (idusuario,)
        users_with_id = self.executeSQL(query, variables)
        if len(users_with_id) > 0:
            return True
        else:
            return False

    def exists_offers_type_sell_with_userid(self, userid: int):
        query = "SELECT * FROM oferta WHERE ofertante = %s AND tipo = 'venta';"
        offers = self.executeSQL(query, (userid,))
        if len(offers) > 0:
            return True
        else:
            return False

    # HU: Obtener productos que se están vendiendo por la tienda
    def get_products_selling_by_shop(self):
        idshop = 8
        if self.exists_offers_type_sell_with_userid(idshop):
            query = "SELECT o.*, p.* FROM producto p INNER JOIN oferta o ON p.idproducto = o.producto_idproducto" \
                    " WHERE o.tipo = 'venta' AND o.ofertante = %s AND (o.estado = 'pendiente_cliente' OR " \
                    " o.estado = 'pendiente_tienda');"
            offers = self.executeSQL(query, (idshop,))
            if len(offers) > 0:
                return offers
            else:
                return []
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offers by shop with this type was not found")

    #HU: Obtener ofertas de compra en proceso de la tienda
    def get_buy_offers_by_shop_process_state(self):
        idtienda = 8
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                " WHERE o.ofertante = %s AND o.estado = 'en_curso' AND o.tipo = 'compra';"
        buys = self.executeSQL(query, (idtienda,))
        if len(buys) > 0:
            return buys
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Buys by shop with this state was not found")

    #HU: Obtener ofertas de compra en proceso de la tienda
    def get_buys_offers_by_shop_process_state(self):
        idtienda = 8
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto"\
                " WHERE o.ofertante = %s AND o.estado = 'en_curso' AND o.tipo = 'compra';"
        buys = self.executeSQL(query, (idtienda,))
        if len(buys) > 0:
            return buys
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Buys by shop with this state was not found")

    # HU: Obtener ofertas de empeño en proceso de la tienda
    def get_pawns_offers_by_shop_process_state(self):
        idtienda = 8
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto"\
                " WHERE o.ofertante = %s AND o.estado = 'en_curso' AND o.tipo = 'empennio';"
        pawns = self.executeSQL(query, (idtienda,))
        if len(pawns) > 0:
            return pawns
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pawns by shop with this state was not found")

    #HU: Obtener ofertas de venta en proceso de la tienda
    def get_sells_offers_by_shop_process_state(self):
        idtienda = 8
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto"\
                " WHERE o.ofertante = %s AND o.estado = 'en_curso' AND o.tipo = 'venta';"
        sells = self.executeSQL(query, (idtienda,))
        if len(sells) > 0:
            return sells
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Sells by shop with this state was not found")

    # HU: Obtener ofertas de empeño en pendiente de la tienda

    def get_pawns_offers_by_shop_in_peding_state(self):
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto"\
                " WHERE (o.estado = 'pendiente_cliente' OR  o.estado = 'pendiente_tienda') AND o.tipo = 'empennio';"
        pawns = self.executeSQL(query)
        if len(pawns) > 0:
            return pawns
        else:
            return []

    def get_all_pawn_on_the_way_offers(self):
        query = "SELECT o.*, p.* FROM OFERTA o INNER JOIN PRODUCTO p ON o.producto_idproducto = p.idproducto"\
                " WHERE o.estado = 'en_curso' AND o.tipo = 'empennio';"
        offers = self.executeSQL(query)
        if len(offers)>0:
            return offers
        else:
            return []

    def get_all_sell_offers_on_the_way(self):
        query = "SELECT o.*, p.* FROM OFERTA o INNER JOIN PRODUCTO p ON o.producto_idproducto = p.idproducto"\
                " WHERE o.estado = 'en_curso' AND o.tipo = 'venta';"
        offers = self.executeSQL(query)
        if len(offers)>0:
            return offers
        else:
            return []



    def add_offer(self, tipo: str, precio: str, producto_idproducto: int, estado: str, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query = "INSERT INTO `mydb`.`oferta` (`tipo`,`precio`,`producto_idproducto`,`estado`,`ofertante`)" \
                        " VALUES (%s,%s, %s,%s,%s);"
                variables = (tipo, precio, producto_idproducto, estado, usuario_idusuario,)
                self.executeSQL(query, variables)
                query_2 = "SELECT * FROM oferta ORDER BY idoferta DESC LIMIT 1;"
                element = self.executeSQL(query_2)
                return element
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    def exists_idoffer(self, idoferta: int):
        query = "SELECT * FROM oferta WHERE idoferta = %s;"
        variables = (idoferta,)
        offers_with_id = self.executeSQL(query, variables)
        if len(offers_with_id) > 0:
            return True
        else:
            return False

    #DELETE OFFER (Falta probar)
    def delete_offer(self, idoferta: int):
        if self.exists_idoffer(idoferta):
            query = "DELETE FROM `mydb`.`oferta` WHERE idoferta = %s"
            variables = (idoferta,)
            self.executeSQL(query, variables)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer with this id was not found")

    #UPDATE OFFER (Falta probar)
    def update_offer(self, nuevo_tipo: str, nuevo_precio: str, nuevo_producto_idproducto: int, nuevo_estado: str,
                     nuevo_usuario_idusuario: int, idoferta: int, producto_idproducto: int, usuario_idusuario: int):

        if self.exists_idoffer(idoferta):
            if self.exists_iduser(nuevo_usuario_idusuario) and self.exists_iduser(usuario_idusuario):
                if self.exists_idproduct(nuevo_producto_idproducto) and self.exists_idproduct(producto_idproducto):
                    query = "UPDATE `mydb`.`oferta` SET `tipo` = %s, `precio` = %s, `producto_idproducto` = %s, " \
                            "estado` = %s, `ofertante` = %s WHERE `idoferta` = %s " \
                            "AND `producto_idproducto` = %s AND `ofertante` = %s;"
                    variables = (nuevo_tipo, nuevo_precio, nuevo_producto_idproducto, nuevo_estado,
                                 nuevo_usuario_idusuario, idoferta, producto_idproducto, usuario_idusuario,)
                    self.executeSQL(query, variables)
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with old id or product with new id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with old id or user with new id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offer with this id was not found")

    #BUY
    def get_buy_by_id(self, idcompra: int):
        if self.buy_with_this_id_exist(idcompra):
            query = "SELECT * FROM COMPRA c WHERE c.idcompra = %s;"
            buy = self.executeSQL(query, (idcompra,))
            return buy[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy with this id was not found")

    def buy_with_this_id_exist(self, idcompra: int):
        query = "SELECT * FROM COMPRA c WHERE c.idcompra = %s;"
        buy = self.executeSQL(query, (idcompra,))
        if len(buy) > 0:
            return True
        else:
            return False

    def delete_buy(self, idcompra: int):
        if not self.buy_with_this_id_exist(idcompra):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Buy with this id does not exist")
        else:
            query = "DELETE FROM `mydb`.`COMPRA` WHERE `idcompra` = %s;"
            variables = (idcompra,)
            self.executeSQL(query, variables)

    def buy_with_this_user_id_exists(self, idusuario: int):
        query = "SELECT * FROM COMPRA c WHERE c.usuario_idusuario = %s;"
        buy = self.executeSQL(query, (idusuario,))
        if len(buy) > 0:
            return True
        else:
            return False

    def update_buy(self, n_precio: int, n_fecha: str, n_usuario_idusuario: int,
                   n_producto_idproducto: int, idcompra: int, usuario_idusuario: int, producto_idproducto: int):
        if not self.buy_with_this_id_exist(idcompra):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Buy with this id does not exist")
        else:
            if self.exists_iduser(usuario_idusuario) and self.exists_iduser(n_usuario_idusuario):
                if self.exists_idproduct(producto_idproducto) and self.exists_idproduct(n_producto_idproducto):
                    if self.check_date(n_fecha):
                        query = "UPDATE `mydb`.`COMPRA` SET  `precio` = %s, `fecha` = %s, `usuario_idusuario` = %s, " \
                                "`producto_idproducto` = %s WHERE `idcompra` = %s AND `usuario_idusuario` = %s " \
                                "AND producto_idproducto = %s;"
                        variables = (n_precio, n_fecha, n_usuario_idusuario, n_producto_idproducto, idcompra,
                                     usuario_idusuario, producto_idproducto)
                        self.executeSQL(query, variables)
                    else:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail="Date entered incorrectly (Y-m-d)")
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with old id or product with new id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with old id or user with new id was not found")

    def get_shopping_by_user_id(self, idusuario: int):
        if not self.get_user_by_id(idusuario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")
        else:
            query = "SELECT c.*, p.* FROM COMPRA c INNER JOIN producto p ON c.producto_idproducto = p.idproducto"\
                    " WHERE c.usuario_idusuario = %s;"
            variables = (idusuario,)
            buys = self.executeSQL(query, variables)
            if len(buys) > 0:
                return buys
            else:
                return []

    def get_buys(self):
        query = "SELECT * FROM COMPRA;"
        buys = self.executeSQL(query)
        return buys

    #SELL
    def get_sell_by_id(self, idventa: int):
        query = "SELECT * FROM VENTA v WHERE v.idventa = %s;"
        sell = self.executeSQL(query, (idventa,))
        if len(sell) > 0:
            return sell[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sell with this id was not found")

    def sell_with_user_id_exist(self, idusuario: int):
        query = "SELECT * FROM venta WHERE usuario_idusuario = %s"
        variables = (idusuario,)
        sells = self.executeSQL(query, variables)
        if len(sells) > 0:
            return True
        else:
            return False

    # HU: Obtener las ofertas de tipo venta , en estado pendiente_cliente  de la tienda
    def get_sells_offers_in_client_peding_state(self):
        idusuario = 8
        if self.exists_shop_type_user_with_this_id(idusuario):
            query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON o.producto_idproducto = p.idproducto" \
                    " WHERE o.usuario_idusuario = %s AND o.tipo = 'venta' AND o.estado = 'pendiente_cliente';"
            variables = (idusuario,)
            sells = self.executeSQL(query, variables)
            if len(sells) > 0:
                return sells
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Sells with this id was not found in shop type users")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with this id was not found in shop type users")

    #HU: Obtener las ventas de un usuario
    def get_sells_by_userid(self, idusuario: int):
        if self.sell_with_user_id_exist(idusuario):
            query = "SELECT * FROM venta v INNER JOIN producto p ON v.producto_idproducto = p.idproducto"\
                    " WHERE v.usuario_idusuario = %s;"
            variables = (idusuario,)
            sells = self.executeSQL(query, variables)
            return sells
        else:
            return []

    def exists_idsell(self, idventa):
        query = "SELECT * FROM venta WHERE idventa = %s;"
        variables = (idventa,)
        sells = self.executeSQL(query, variables)
        if len(sells) > 0:
            return True
        else:
            return False

    #CREATE SELL (falta probar)
    def add_sell(self, precio: int, fecha: str, usuario_idusuario: int, producto_idproducto: int,
                 id_factura_compraventa: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha):
                    self.get_bill_buy_sell_by_id(id_factura_compraventa)
                    query = "INSERT INTO `mydb`.`VENTA` (`precio`,`fecha`,`usuario_idusuario`,`producto_idproducto`, `facturacompraventa_idFacturaCompra`) " \
                            "VALUES (%s,%s,%s,%s, %s);"
                    variables = (precio, fecha, usuario_idusuario, producto_idproducto, id_factura_compraventa)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM venta ORDER BY idventa DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element[0]
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail="Date entered incorrectly (Y-m-d)")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    def add_buy(self, precio: int, fecha: str, usuario_idusuario: int, producto_idproducto: int,
                id_factura_compraventa: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha):
                    self.get_bill_buy_sell_by_id(id_factura_compraventa)
                    query = "INSERT INTO `mydb`.`compra` (`precio`,`fecha`,`usuario_idusuario`,`producto_idproducto`, `facturacompraventa_idFacturaCompra`) " \
                            "VALUES (%s,%s,%s,%s, %s);"
                    variables = (precio, fecha, usuario_idusuario, producto_idproducto, id_factura_compraventa)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM compra ORDER BY idcompra DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element[0]
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail="Date entered incorrectly (Y-m-d)")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    #DELETE SELL (sin probar)
    def delete_sell(self, idventa: int):
        if not self.exists_idsell(idventa):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Sell with this id does not exist")
        else:
            query = "DELETE FROM `mydb`.`VENTA` WHERE `idventa` = %s;"
            variables = (idventa,)
            self.executeSQL(query, variables)

    #UPDATE SELL
    def update_sell(self, n_precio: int, n_fecha: str, n_usuario_idusuario: int,
                    n_producto_idproducto: int, idventa: int, usuario_idusuario: int, producto_idproducto: int):
        if not self.exists_idsell(idventa):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Sell with this id does not exist")
        else:
            if self.exists_iduser(usuario_idusuario) and self.exists_iduser(n_usuario_idusuario):
                if self.exists_idproduct(producto_idproducto) and self.exists_idproduct(n_producto_idproducto):
                    if self.check_date(n_fecha):
                        query = "UPDATE `mydb`.`COMPRA` SET  `precio` = %s, `fecha` = %s, `usuario_idusuario` = %s," \
                                "`producto_idproducto` = %s WHERE `idventa` = %s AND `usuario_idusuario` = %s " \
                                "AND producto_idproducto = %s;"
                        variables = (n_precio, n_fecha, n_usuario_idusuario, n_producto_idproducto, idventa,
                                     usuario_idusuario, producto_idproducto)
                        self.executeSQL(query, variables)
                    else:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail="Date entered incorrectly (Y-m-d)")
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with old id or product with new id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with old id or user with new id was not found")

    def exists_offers_with_userid(self, idusuario: int):
        query = "SELECT * FROM oferta WHERE usuario_idusuario = %s;"
        offers = self.executeSQL(query, (idusuario,))
        if len(offers) > 0:
            return True
        else:
            return False

    #HU: Obtener las ofertas de empeño desde el punto de vista de la tienda (falta revisarlo)
    def get_pawn_offers_by_shop(self):
        idshop = 8
        if self.exists_offers_with_userid(idshop):
            query = "SELECT * FROM oferta WHERE usuario_idusuario = %s AND tipo = 'empennio';"
            pawns = self.executeSQL(query, (idshop,))
            if len(pawns) > 0:
                return pawns
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Offers by shop whit this type was not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Offers by shop was not found")

        #PAWN

    def exists_pawn_with_userid(self, idusuario: int):
        query = "SELECT * FROM empennio WHERE usuario_idusuario = %s;"
        pawns = self.executeSQL(query, (idusuario,))
        if len(pawns) > 0:
            return True
        else:
            return False

    # HU: Obtener mis empeños vigentes
    def get_currents_pawns_by_userid(self, idusuario: int):
        if self.get_user_by_id(idusuario):
            query = "SELECT e.*, p.* FROM empennio e INNER JOIN producto p ON e.producto_idproducto = p.idproducto"\
                    " WHERE e.usuario_idusuario = %s AND e.estado = 'en_curso';"
            pawns = self.executeSQL(query, (idusuario,))
            if len(pawns) > 0:
                return pawns
            else:
                return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pawns with this user id was not found")

    def get_pawns_by_userid(self, idusuario: int):
        if self.get_user_by_id(idusuario):
            query = "SELECT e.*, p.* FROM empennio e INNER JOIN producto p ON e.producto_idproducto = p.idproducto"\
                    " WHERE e.usuario_idusuario = %s;"
            pawns = self.executeSQL(query, (idusuario,))
            if len(pawns) > 0:
                return pawns
            else:
                return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pawns with this user id was not found")

    # HU: Obtener los empeños vigentes de la tienda
    def get_currents_pawns_by_shop(self):
        query = "SELECT * FROM empennio WHERE  estado = 'en_curso';"
        pawns = self.executeSQL(query)
        if len(pawns) > 0:
            return pawns
        elif len(pawns) == 0:
            return []

    def exists_idpawn(self, idempennio):
        query = "SELECT * FROM empennio WHERE idempennio = %s;"
        pawns = self.executeSQL(query, (idempennio,))
        if len(pawns) > 0:
            return True
        else:
            return False

    def get_pawn_by_id(self, idempennio: int):
        query = "SELECT * FROM EMPENNIO p WHERE p.idempennio = %s;"
        pawn = self.executeSQL(query, (idempennio,))
        if len(pawn) > 0:
            return pawn[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pawn with this id was not found")

    #CREATE PAWN (falta probar)
    def add_pawn(self, precio: int, fecha_inicio: str, fecha_final: str, usuario_idusuario: int,
                 producto_idproducto: int, factura_empennio: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha_inicio) and self.check_date(fecha_final):
                    self.get_bill_pawn_by_id(factura_empennio)
                    query = "INSERT INTO `mydb`.`EMPENNIO` (`precio`,`estado`, `fecha_inicio`, `fecha_final`," \
                            " `interes`, `usuario_idusuario`, `producto_idproducto`, `facturaempennio_idFacturaEmpennio`) VALUES (%s,%s,%s,%s,%s,%s,%s, %s);"
                    variables = (precio, "en_curso", fecha_inicio, fecha_final, 5, usuario_idusuario,
                                 producto_idproducto, factura_empennio)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM empennio ORDER BY idempennio DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element[0]
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail="Initial date or final date entered incorrectly (Y-m-d)")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    #DELETE PAWN (falta probar)
    def delete_pawn(self, idempennio: int):
        if not self.exists_idpawn(idempennio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pawn with this id does not exist")
        else:
            query = "DELETE FROM `mydb`.`EMPENNIO` WHERE `idempennio` = %s;"
            variables = (idempennio,)
            self.executeSQL(query, variables)

    def pay_pawn(self, id_pawn, id_pago_factura_empennio):
        if not self.exists_idpawn(id_pawn):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pawn with this id does not exist")
        self.get_bill_pay_pawn_by_id(id_pago_factura_empennio)
        query = "UPDATE `mydb`.`EMPENNIO` SET  `estado` = %s , `facturapagoempennio_idFacturaEmpennio` = %s WHERE `idempennio` = %s ;"
        variables = ("pagado", id_pago_factura_empennio, id_pawn)
        self.executeSQL(query, variables)
        return self.get_pawn_by_id(id_pawn)

    def finish_offer(self, id_offer):
        if not self.get_offer_by_id(id_offer):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offer with this id does not exist")
        else:
            query = "UPDATE `mydb`.`OFERTA` SET  `estado` = %s WHERE `idoferta` = %s ;"
            variables = ("finalizada", id_offer)
            self.executeSQL(query, variables)
            return self.get_offer_by_id(id_offer)

    def update_offer_state(self, id_offer, state : str):
        if not self.get_offer_by_id(id_offer):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Offer with this id does not exist")
        else:
            query = "UPDATE `mydb`.`OFERTA` SET  `estado` = %s WHERE `idoferta` = %s ;"
            variables = (state, id_offer)
            self.executeSQL(query, variables)
            return self.get_offer_by_id(id_offer)

    def get_offer_by_id(self, idoferta: int):
        if self.exists_idoffer(idoferta):
            query = "SELECT * FROM OFERTA o WHERE o.idoferta = %s;"
            oferta = self.executeSQL(query, (idoferta,))
            return oferta[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer with this id was not found")

    #UPDATE PAWN (falta probar)
    def update_pawn(self, n_precio: int, n_estado: str, n_fecha_inicio: str, n_fecha_final: str, n_interes: str,
                    n_usuario_idusuario: int, n_producto_idproducto: int, idempennio: int, usuario_idusuario: int,
                    producto_idproducto: int, id_pago_factura_empennio):
        if not self.exists_idpawn(idempennio):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pawn with this id does not exist")
        else:
            if self.exists_iduser(usuario_idusuario) and self.exists_iduser(n_usuario_idusuario):
                if self.exists_idproduct(producto_idproducto) and self.exists_idproduct(n_producto_idproducto):
                    if self.check_date(n_fecha_inicio) and self.check_date(n_fecha_final):
                        query = "UPDATE `mydb`.`EMPENNIO` SET  `precio` = %s, `estado` = %s, `fecha_inicio` = %s," \
                                " `fecha_final` = %s, `interes` = %s, `usuario_idusuario` = %s," \
                                "`producto_idproducto` = %s WHERE `idempennio` = %s AND `usuario_idusuario` = %s " \
                                "AND producto_idproducto = %s;"
                        variables = (n_precio, n_estado, n_fecha_inicio, n_fecha_final, n_interes, n_usuario_idusuario,
                                     n_producto_idproducto, idempennio, usuario_idusuario, producto_idproducto)
                        self.executeSQL(query, variables)
                    else:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                            detail="Date entered incorrectly (Y-m-d)")
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Product with old id or product with new id was not found")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with old id or user with new id was not found")

    #Bill_buy_sell
    def add_bill_buy_sell(self, medio_pago: str, total: int, nombres: str, apellidos: str, direccion: str,
                          departamento: str, municipio: str, telefono: str, correo: str, precio_envio: int,
                          precio_IVA: int, info_adicional: str):
        query = "INSERT INTO `mydb`.`facturacompraventa` (`medio_pago`, `total`, `nombres`, `apellidos`, `direccion`," \
                " `departamento`, `municipio`, `telefono`, `correo`, `precio_envio`, `precio_IVA`, `info_adicional` )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        variables = (medio_pago, total, nombres, apellidos, direccion, departamento, municipio, telefono, correo,
                     precio_envio, precio_IVA, info_adicional)
        self.executeSQL(query, variables)
        query_2 = "SELECT * FROM facturacompraventa ORDER BY idFacturaCompra DESC LIMIT 1;"
        element = self.executeSQL(query_2)
        return element[0]

    def get_bill_buy_sell_by_id(self, idBill: int):
        query = "SELECT * FROM facturacompraventa WHERE idFacturaCompra = %s;"
        variables = (idBill,)
        element = self.executeSQL(query, variables)
        if len(element) > 0:
            return element[0]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill with this id was not found")

    def get_bill_pawn_by_id(self, idBill: int):
        query = "SELECT * FROM facturaempennio WHERE idFacturaEmpennio = %s;"
        variables = (idBill,)
        element = self.executeSQL(query, variables)
        if len(element) > 0:
            return element[0]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill with this id was not found")

    def get_bill_pay_pawn_by_id(self, idBill: int):
        query = "SELECT * FROM facturapagoempennio WHERE idFacturaEmpennio = %s;"
        variables = (idBill,)
        element = self.executeSQL(query, variables)
        if len(element) > 0:
            return element[0]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill with this id was not found")

    def add_bill_pawn(self, medio_pago: str, total: int, nombres: str, apellidos: str, direccion: str,
                      departamento: str, municipio: str, telefono: str, correo: str, precio_envio: int,
                      precio_IVA: int, info_adicional: str):
        query = "INSERT INTO `mydb`.`facturaempennio` (`medio_pago`, `total`, `nombres`, `apellidos`, `direccion`," \
                " `departamento`, `municipio`, `telefono`, `correo`, `precio_envio`, `precio_IVA`, `info_adicional` )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        variables = (medio_pago, total, nombres, apellidos, direccion, departamento, municipio, telefono, correo,
                     precio_envio, precio_IVA, info_adicional)
        self.executeSQL(query, variables)
        query_2 = "SELECT * FROM facturaempennio ORDER BY idFacturaEmpennio DESC LIMIT 1;"
        element = self.executeSQL(query_2)
        return element[0]

    def add_bill_pay_pawn(self, medio_pago: str, total: int, nombres: str, apellidos: str, direccion: str,
                          departamento: str, municipio: str, telefono: str, correo: str, precio_envio: int,
                          precio_IVA: int, info_adicional: str):
        query = "INSERT INTO `mydb`.`facturapagoempennio` (`medio_pago`, `total`, `nombres`, `apellidos`, `direccion`," \
                " `departamento`, `municipio`, `telefono`, `correo`, `precio_envio`, `precio_IVA`, `info_adicional` )VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        variables = (medio_pago, total, nombres, apellidos, direccion, departamento, municipio, telefono, correo,
                     precio_envio, precio_IVA, info_adicional)
        self.executeSQL(query, variables)
        query_2 = "SELECT * FROM facturapagoempennio ORDER BY idFacturaEmpennio DESC LIMIT 1;"
        element = self.executeSQL(query_2)
        return element[0]

    @staticmethod
    def check_date(date: str) -> bool:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
