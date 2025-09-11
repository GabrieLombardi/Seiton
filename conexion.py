from tabulate import tabulate
import mysql.connector

# Conectarse al servidor MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="LombardiG369",
    database="pedidos",
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM ciudad")
filas = cursor.fetchall()

# Mostrar en forma de tabla
print(tabulate(filas, headers=["ID", "ciudad", "cod_postal"], tablefmt="fancy_grid"))

conn.close()