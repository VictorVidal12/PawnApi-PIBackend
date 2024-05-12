from fastapi import HTTPException, status
import mysql.connector

config = {'user': 'myadmin',
          'host': 'serverflexibletest.mysql.database.azure.com',
          'password': 'HolaMundo*',
          'database': 'mydb',
          'port': 3306,  # Puerto predeterminado de MySQL
          'raise_on_warnings': True}  # Para que se generen excepciones en caso de advertencias


class ConnectionDB:
    conn = None  # Mantén la conexión abierta en la instancia

    def __init__(self):
        pass

    def executeSQL(self, consulta_sql, variables_adicionales=None):
        try:
            conn = mysql.connector.connect(**config)  # Abre la conexión si no está abierta

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(consulta_sql, variables_adicionales)

                if consulta_sql.strip().upper().startswith("INSERT") or consulta_sql.strip().upper().startswith(
                        "UPDATE") or consulta_sql.strip().upper().startswith(
                    "DELETE") or consulta_sql.strip().upper().startswith("CREATE"):
                    conn.commit()
                    return None

                resultados = cursor.fetchall()
                conn.close()
                return resultados
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)

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

    def add_user(self, nombre: str, correo_electronico: str, contrasennia: str, tipo: str):
        if self.user_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post an User  with an existing email")
        else:
            query = "INSERT INTO `mydb`.`USUARIO` (`nombre`,`correo_electronico`,`contrasennia`,`tipo`) " \
                    "VALUES (%s,%s,%s,%s);"
            variables = (nombre, correo_electronico, contrasennia, tipo)
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


    #PRODUCTO
    def get_product_by_id(self, idproducto : int):
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

    def get_product_by_image(self, image :str):
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
            self.executeSQL(query,variables)

    def update_product_image(self, idproducto: int, imagen: str):
        if not self.product_with_this_id_exist(idproducto):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product with this id does not exist")
        else:
            query = "UPDATE `mydb`.`PRODUCTO` SET  `imagen` = %s " \
                    "WHERE `idproducto` = %s;"
            variables = (imagen, idproducto,)
            self.executeSQL(query,variables)

    def product_with_this_id_exist(self, idproducto):
        query = "SELECT * FROM PRODUCTO p WHERE p.idproducto = %s;"
        product = self.executeSQL(query, (idproducto,))
        if len(product) > 0:
            return True
        else:
            return False
