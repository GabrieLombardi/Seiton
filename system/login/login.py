from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.Button_instrucciones_uso.clicked.connect(self.abrir_instrucciones)

    def abrir_instrucciones(self):
        self.instrucciones = uic.loadUi("instrucciones.ui")
        # Asigna el texto al QLabel
        self.instrucciones.label_text.setText(
            "Esta es la penstaña para iniciar sesión en el programa.\n"
            "Lo primero que debes de hacer es Rellenar los cuadros de texto con los datos de tu usuario y contraseña.\n"
            "Al presionar el botón de continuar se ingresara al menú principal del programa."
        )
        # Asigna la imagen al QLabel
        # self.instrucciones.label_img.setPixmap(QPixmap("C:/Users/GAYBRIEL/Desktop/2025/Practica Profesional I/Seiton/system/login/txt_img.png"))
        self.instrucciones.show()

if __name__ == "__main__":
    app = QApplication([])
    ventana = LoginWindow()
    ventana.show()
    app.exec_()