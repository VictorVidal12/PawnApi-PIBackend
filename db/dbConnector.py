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

    #FALTA PROBARLO
    def get_pending_pawn_offerts_by_userid(self, idusuario: int):
        query = "SELECT o.*, p.* FROM oferta o INNER JOIN producto p ON p.idproducto = o.producto_idproducto WHERE " \
                " o.estado = 'Pendiente Tienda' AND o.usuario_idusuario = %s AND o.tipo = 'empennio';"
        variables = (idusuario,)
        list_offerts = self.executeSQL(query, variables)
        if len(list_offerts) > 0:
            return list_offerts
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="This user does not have pending pawn offerts.")

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email was not found")

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
    # El cliente crea la oferta
    # HU: Crear oferta de empeño(cliente)
    def add_offer_type_pawn_by_client(self, precio: str, producto_idproducto: int, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query_1 = "INSERT INTO `mydb`.`oferta` VALUES ('empennio',%s,'pendiente_tienda',%s,%s);"
                variables_1 = (precio, producto_idproducto, usuario_idusuario,)
                self.executeSQL(query_1, variables_1)
                query_2 = "SELECT * FROM oferta ORDER BY idoferta DESC LIMIT 1;"
                element = self.executeSQL(query_2)
                return element
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    # El cliente crea la oferta
    # HU: Crear oferta de venta (cliente)
    def add_offer_type_sell_by_client(self, precio: str, producto_idproducto: int, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query = "INSERT INTO `mydb`.`oferta` VALUES ('venta',%s,'pendiente_tienda',%s,%s);"
                variables = (precio, producto_idproducto, usuario_idusuario,)
                self.executeSQL(query, variables)
                query_2 = "SELECT * FROM oferta ORDER BY idoferta DESC LIMIT 1;"
                element = self.executeSQL(query_2)
                return element
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    # HU: Actualizar oferta para contraofertar el precio (cliente)
    def update_offer_with_counteroffer_client(self, contra_oferta: str, idoferta, usuario_idusuario,
                                              producto_idproducto):
        if self.exists_idoffer(idoferta):
            if self.exists_client_type_user_with_this_id(usuario_idusuario):
                if self.exists_idproduct(producto_idproducto):
                    query = "UPDATE `mydb`.`oferta` SET `precio` = %s, estado` = 'pendiente_tienda' " \
                            "WHERE `idoferta` = %s AND `producto_idproducto` = %s AND `usuario_idusuario` = %s;"
                    variables = (contra_oferta, idoferta, producto_idproducto, usuario_idusuario,)
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

    # HU: Actualizar oferta para contraofertar el precio (tienda)
    def update_offer_with_counteroffer_shop(self, contra_oferta: str, idoferta, usuario_idusuario,
                                            producto_idproducto):
        if self.exists_idoffer(idoferta):
            if self.exists_shop_type_user_with_this_id(usuario_idusuario):
                if self.exists_idproduct(producto_idproducto):
                    query = "UPDATE `mydb`.`oferta` SET `precio` = %s, estado` = 'pendiente_cliente' " \
                            "WHERE `idoferta` = %s AND `producto_idproducto` = %s AND `usuario_idusuario` = %s;"
                    variables = (contra_oferta, idoferta, producto_idproducto, usuario_idusuario,)
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

    #CREATE OFFER (Falta Probar)
    def add_offer(self, tipo: str, precio: str, producto_idproducto: int, estado: str, usuario_idusuario: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                query = "INSERT INTO `mydb`.`oferta` VALUES (%s,%s, %s,%s,%s);"
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
                            "estado` = %s, `usuario_idusuario` = %s WHERE `idoferta` = %s " \
                            "AND `producto_idproducto` = %s AND `usuario_idusuario` = %s;"
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

    def get_buys_by_id_shop(self, idcompra: int):
        pass

    def add_buy(self, precio: int, fecha: str, usuario_idusuario: int, producto_idproducto: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha):
                    query = "INSERT INTO `mydb`.`COMPRA` (`precio`,`fecha`,`usuario_idusuario`,`producto_idproducto`) "\
                            "VALUES (%s,%s,%s,%s);"
                    variables = (precio, fecha, usuario_idusuario, producto_idproducto)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM compra ORDER BY idcompra DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail="Date entered incorrectly (Y-m-d)")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this id was not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

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

    def get_buy_by_user_id(self, idusuario: int):
        if not self.buy_with_this_user_id_exists(idusuario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy with this id was not found")
        else:
            query = "SELECT * FROM COMPRA c WHERE c.usuario_idusuario = %s;"
            variables = (idusuario,)
            buys = self.executeSQL(query, variables)
            return buys

    def get_buys(self):
        query = "SELECT * FROM COMPRA;"
        buys = self.executeSQL(query)
        if len(buys) > 0:
            return buys
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buys was not found")

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

    # HU: Obtener productos que la tienda está vendiendo (con id)
    def get_shop_sells_with_id(self, idusuario: int):
        if self.exists_shop_type_user_with_this_id(idusuario):
            query = "SELECT p.* FROM venta v INNER JOIN producto p ON v.usuario_idusuario = p.usuario_idusuario" \
                    "WHERE v.usuario_idusuario = %s;"
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

    def get_sells_with_userid(self, idusuario: int):
        if self.sell_with_user_id_exist(idusuario):
            query = "SELECT * FROM venta WHERE usuario_idusuario = %s"
            variables = (idusuario,)
            sells = self.executeSQL(query, variables)
            return sells
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id was not found")

    def exists_idsell(self, idventa):
        query = "SELECT * FROM venta WHERE idventa = %s;"
        variables = (idventa,)
        sells = self.executeSQL(query, variables)
        if len(sells) > 0:
            return True
        else:
            return False

    #CREATE SELL (falta probar)
    def add_sell(self, precio: int, fecha: str, usuario_idusuario: int, producto_idproducto: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha):
                    query = "INSERT INTO `mydb`.`VENTA` (`precio`,`fecha`,`usuario_idusuario`,`producto_idproducto`) " \
                            "VALUES (%s,%s,%s,%s);"
                    variables = (precio, fecha, usuario_idusuario, producto_idproducto)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM venta ORDER BY idventa DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element
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

    #PAWN

    def exists_idpawn(self, idempennio):
        query = "SELECT * FROM empennio WHERE idempennio = %s;"
        pawns = self.executeSQL(query, (idempennio,))
        if len(pawns) > 0:
            return True
        else:
            return False

    def get_pawn_by_id(self, idempennio: int):
        query = "SELECT * FROM PRESTAMO p WHERE p.idprestamo = %s;"
        pawn = self.executeSQL(query, (idempennio,))
        if len(pawn) > 0:
            return pawn[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pawn with this id was not found")

    #CREATE PAWN (falta probar)
    def add_pawn(self, precio: int, estado: str, fecha_inicio: str, fecha_final: str,
                 interes: int, usuario_idusuario: int, producto_idproducto: int):
        if self.exists_iduser(usuario_idusuario):
            if self.exists_idproduct(producto_idproducto):
                if self.check_date(fecha_inicio) and self.check_date(fecha_final):
                    query = "INSERT INTO `mydb`.`EMPENNIO` (`precio`,`estado`, `fecha_inicio`, `fecha_final`," \
                            " `interes`, `usuario_idusuario`, `producto_idproducto`) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                    variables = (precio, estado, fecha_inicio, fecha_final, interes, usuario_idusuario,
                                 producto_idproducto)
                    self.executeSQL(query, variables)
                    query_2 = "SELECT * FROM empennio ORDER BY idempennio DESC LIMIT 1;"
                    element = self.executeSQL(query_2)
                    return element
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

    #UPDATE PAWN (falta probar)
    def update_pawn(self, n_precio: int, n_estado: str, n_fecha_inicio: str, n_fecha_final: str, n_interes: str,
                    n_usuario_idusuario: int, n_producto_idproducto: int, idempennio: int, usuario_idusuario: int,
                    producto_idproducto: int):
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

    @staticmethod
    def check_date(date: str) -> bool:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
