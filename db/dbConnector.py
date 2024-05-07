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

    def get_clients(self):
        query = "SELECT * FROM CLIENTE"
        owners = self.executeSQL(query)
        return owners
    def get_client_by_email(self,email):
        query = "SELECT * FROM CLIENTE c WHERE c.correo_electronico = %s;"
        client = self.executeSQL(query, (email,))
        if len(client) > 0:
            return client[0]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client with this email was not found")

    def add_client(self, nombre: str, nombre_usuario: str, correo_electronico: str, contrasennia: str, edad: str, genero: str):
        # Verificar si no existe un correo igual
        if self.client_with_this_email_exist(correo_electronico):
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                                detail="You cannot post a Client  with an existing email")
        else:
            query = "INSERT INTO `mydb`.`cliente` (`nombre`,`nombre_usuario`,`correo_electronico`,`contrasennia`, `edad`, `genero`) " \
                    "VALUES (%s,%s,%s,%s, %s, %s);"
            variables = (nombre, nombre_usuario, correo_electronico, contrasennia,int(edad),genero)
            self.executeSQL(query, variables)





    def client_with_this_email_exist(self, correo):
        query = "SELECT * FROM CLIENTE c WHERE c.correo_electronico = %s;"
        client = self.executeSQL(query, (correo,))
        if len(client) > 0:
            return True
        else:
            return False
