from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sqlite3
import sys

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # Usar rutas basadas en __file__
        ui_path = Path(__file__).resolve().parents[2] / "main.ui"
        uic.loadUi(str(ui_path), self)
        
        if hasattr(self, 'pushButton_2'):
            self.pushButton_2.clicked.connect(self.abrir_menu)

    def abrir_menu(self):
        # Simple verification: read usuario and contraseña from the UI
        try:
            usuario = self.lineEdit.text().strip()
            contrasena = self.lineEdit_2.text().strip()
        except Exception:
            QMessageBox.warning(self, "Login", "No se encontraron los campos de usuario/contraseña en la UI")
            return

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Login", "Complete usuario y contraseña")
            return

        # Verificar en la base de datos pedidos.sqlite3
        db_path = Path(__file__).resolve().parents[2] / "pedidos.sqlite3"
        try:
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()
            cur.execute('SELECT id_acceso FROM login WHERE usuario = ? AND "contraseña" = ?;', (usuario, contrasena))
            row = cur.fetchone()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error BD", f"Error accediendo a la base de datos:\n{e}")
            return

        if row:
            # Credenciales correctas: abrir menú
            self.menu = MenuPrincipal()
            self.menu.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Usuario o contraseña incorrectos")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit.setFocus()

class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = Path(__file__).resolve().parents[2] / "menu_principal.ui"
        uic.loadUi(str(ui_path), self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Main()
    ventana.show()
    sys.exit(app.exec_())