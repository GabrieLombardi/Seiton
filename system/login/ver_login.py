# ...existing code...
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

app = QApplication([])
window = uic.loadUi("main.ui")  # Asegúrate de que el archivo .ui esté en la misma carpeta
window.show()
app.exec_()
# ...existing code...