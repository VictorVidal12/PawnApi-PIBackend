from fastapi import HTTPException, status
import mysql.connector
from mysql.connector import pooling


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
    def get_pending_pawn_offerts_by_userid(self, idusuario):
        query = "SELECT o.* FROM oferta o INNER JOIN producto p ON p.idproducto = o.producto_idproducto INNER JOIN empennio e ON e.producto_idproducto = o.producto_idproducto WHERE  o.estado = 'Pendiente Tienda' AND o.usuario_idusuario = %s;"
        list_offerts = self.executeSQL(query, idusuario)
        if len(list_offerts) > 0:
            return list_offerts
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not have pending pawn offerts.")

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

    def delete_user(self, correo_electronico: str):
        if not self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with this email does not exist")
        else:
            query = "DELETE FROM `mydb`.`USUARIO` WHERE `correo_electronico` = %s;"
            variables = (correo_electronico,)
            self.executeSQL(query, variables)

    def update_user(self, correo_electronico: str, nuevo_nombre: str, nueva_contrasennia: str, nuevo_tipo: str):
        if not self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User with this email does not exist")
        else:
            query = "UPDATE `mydb`.`USUARIO` SET `nombre` = %s, `contrasennia` = %s, `tipo` = %s " \
                    "WHERE `correo_electronico` = %s;"
            variables = (nuevo_nombre, nueva_contrasennia, nuevo_tipo, correo_electronico)
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

    def get_oferta_by_id(self, idoferta: int):
        query = "SELECT * FROM OFERTA o WHERE o.idoferta = %s;"
        oferta = self.executeSQL(query, (idoferta,))
        if len(oferta) > 0:
            return oferta[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer with this id was not found")

    #TODO CREATE OFFER
    def add_offer(self):
        pass

    #TODO DELETE OFFER
    def delete_offer(self):
        pass

    #TODO UPDATE OFFER
    def update_offer(self):
        pass

    #BUY
    def get_buy_by_id(self, idcompra: int):
        query = "SELECT * FROM COMPRA c WHERE c.idcompra = %s;"
        buy = self.executeSQL(query, (idcompra,))
        if len(buy) > 0:
            return buy[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy with this id was not found")

    def add_buy(self, precio: int, fecha: str, medio_pago: str, usuario_idusuario: int, producto_idproducto: int):
        query = "INSERT INTO `mydb`.`COMPRA` (`precio`,`fecha`,`medio_pago`,`usuario_idusuario`,`producto_idproducto`) " \
                "VALUES (%s,%s,%s,%s,%s);"
        variables = (precio, fecha, medio_pago, usuario_idusuario, producto_idproducto)
        self.executeSQL(query, variables)

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

    def update_buy(self, idcompra: int, n_precio: int, n_fecha: str, n_medio_pago: str, n_usuario_idusuario: int,
                   n_producto_idproducto: int):
        if not self.buy_with_this_id_exist(idcompra):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Buy with this id does not exist")
        else:
            query = "UPDATE `mydb`.`COMPRA` SET  `n_precio` = %s, `n_fecha` = %s, `n_medio_pago` = %s, `n_usuario_idusuario` = %s, `n_producto_idproducto` = %s " \
                    "WHERE `idcompra` = %s;"
            variables = (n_precio, n_fecha, n_medio_pago, n_usuario_idusuario, n_producto_idproducto,)
            self.executeSQL(query, variables)

    def get_buy_by_user_email(self, correo: str):
        user = self.get_user_by_email(correo)
        idusuario = user[0]
        if not self.buy_with_this_user_id_exists(idusuario):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy with this email was not found")
        else:
            query = "SELECT * FROM COMPRA c WHERE c.usuario_idusuario = %s;"
            variables = (idusuario,)
            buys = self.executeSQL(query, variables)
            return buys

    def get_buy(self):
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

    #TODO CREATE SELL
    def add_sell(self):
        pass

    #TODO DELETE SELL
    def delete_sell(self):
        pass

    #TODO UPDATE SELL
    def update_sell(self):
        pass

    #PAWN
    def get_pawn_by_id(self, idempennio: int):
        query = "SELECT * FROM PRESTAMO p WHERE p.idprestamo = %s;"
        pawn = self.executeSQL(query, (idempennio,))
        if len(pawn) > 0:
            return pawn[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pawn with this id was not found")

    #TODO CREATE PAWN
    def add_pawn(self):
        pass

    #TODO DELETE PAWN
    def delete_pawn(self):
        pass

    #TODO UPDATE PAWN
    def update_pawn(self):
        pass
