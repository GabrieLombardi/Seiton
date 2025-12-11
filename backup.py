import sqlite3
import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime

# ------------------------------
# 1. Crear backup local de SQLite
# ------------------------------
nombre_db = "pedidos.sqlite3"
backup_nombre = f"pedidosbackup_{datetime.date.today()}.db"

con = sqlite3.connect(nombre_db)
with con:
    con.backup(sqlite3.connect(backup_nombre))

print(f"Backup creado: {backup_nombre}")

# ------------------------------
# 2. Subir backup a Google Drive
# ------------------------------
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Se abre una ventana para iniciar sesión
drive = GoogleDrive(gauth)

archivo_drive = drive.CreateFile({'title': backup_nombre})
archivo_drive.SetContentFile(backup_nombre)
archivo_drive.Upload()

print("Backup subido a Google Drive con éxito.")
