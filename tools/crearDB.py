#Creacion de una base de datos (BD)
import sqlite3 #importo la libreria
miConexion=sqlite3.connect("pedidos.sqlite3") #conecto con la BD
print(miConexion)
miConexion.close() #cierro la conexion

# revisar o ver la BD con el SQLite Database 