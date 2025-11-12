from pathlib import Path
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = Path(__file__).resolve().parents[2] / "main.ui"
        uic.loadUi(str(ui_path), self)
        
        if hasattr(self, 'pushButton_2'):
            self.pushButton_2.clicked.connect(self.abrir_menu)

    def abrir_menu(self):
        menu_ui_path = Path(__file__).resolve().parents[2] / "menu_principal.ui"
        self.menu = uic.loadUi(str(menu_ui_path))
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

