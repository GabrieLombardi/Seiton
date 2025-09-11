# Importamos la biblioteca sqlite3 para interactuar con bases de datos SQLite
import sqlite3

# Definimos una clase llamada CRUD, que contiene métodos para Crear, Leer, Actualizar y Borrar registros en una base de datos.
class CRUD(object): 
    def __init__(self):
        # Este es el constructor de la clase. 
        # Aquí inicializamos las variables que usaremos en los métodos.
        self.miConexion = ""  # Variable para almacenar la conexión a la base de datos
        self.BD = "pedidos.sqlite3"  # Nombre del archivo de la base de datos SQLite
        return  # Fin del constructor

    # Método para crear (insertar) nuevos registros en la base de datos
    def Create(self, _miConsulta, _misDatos):
        miConexion = self.ConectarDB()
        miCursor = miConexion.cursor()

        try:
            # Si los datos son una tupla, ejecuta la consulta.
            if isinstance(_misDatos, tuple):
                miCursor.execute(_miConsulta, _misDatos)
            # Si es una lista de tuplas, usa executemany.
            elif isinstance(_misDatos, list):
                miCursor.executemany(_miConsulta, _misDatos)
            else:
                raise ValueError("Los datos proporcionados no tienen el formato esperado.")
            
            miConexion.commit()
            print('Se guardó satisfactoriamente.')
        except sqlite3.Error as e:
            print("Ha ocurrido un error al crear los datos: ", e)
        finally:
            miCursor.close()
            miConexion.close()

        return  # Fin del método

    # Método para leer datos de la base de datos
    def Read(self, _miConsulta):
        print(_miConsulta)  # Mostramos la consulta que se ejecutará (útil para depuración)
        self.miConexion = self.ConectarDB()  # Nos conectamos a la base de datos
        # Configuramos cómo manejar textos, ignorando errores de codificación
        self.miConexion.text_factory = lambda b: b.decode(errors='ignore')  
        # Ejecutamos la consulta SQL y obtenemos los resultados
        resultado = self.miConexion.execute(_miConsulta)
        return resultado  # Retornamos los resultados para ser utilizados por quien llame al método

    # Método para actualizar registros en la base de datos
    def Update(self, _miConsulta, _misDatos):
        print('dbCrud')  # Mensaje de depuración
        try:
            miConexion = self.ConectarDB()  # Nos conectamos a la base de datos
            miCursor = miConexion.cursor()  # Creamos un cursor para ejecutar consultas SQL
            # Ejecutamos la consulta usando ejecutemany para actualizar múltiples registros
            miCursor.executemany(_miConsulta, _misDatos)
            miConexion.commit()  # Guardamos los cambios
            miCursor.close()  # Cerramos el cursor
            miConexion.close()  # Cerramos la conexión
        except Exception as miError:  # Capturamos cualquier error
            print('Error al editar:', miError)  # Mostramos el error
        return  # Fin del método

    # Método para borrar registros de la base de datos
    def Delete(self, _miConsulta):
        try:
            miConexion = self.ConectarDB()  # Nos conectamos a la base de datos
            miCursor = miConexion.cursor()  # Creamos un cursor
            miCursor.execute(_miConsulta)  # Ejecutamos la consulta SQL para borrar datos
            miConexion.commit()  # Guardamos los cambios
            miCursor.close()  # Cerramos el cursor
            miConexion.close()  # Cerramos la conexión
        except Exception as miError:  # Capturamos errores
            print('Error al borrar:', miError)  # Mostramos el error
        return  # Fin del método

    # Método para establecer una conexión con la base de datos
    def ConectarDB(self):
        return sqlite3.connect(self.BD)  # Devuelve una conexión a la base de datos

    # Método para cerrar la conexión con la base de datos (si está abierta)
    def DesconectarDb(self):
        self.miConexion.close()  # Cierra la conexión
