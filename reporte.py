from PyQt5.QtWidgets import QWidget, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
import os

class Reporte(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('reporte.ui', self)
        self.btn_volver_reporte.clicked.connect(self.volver)
        self.btn_descargar_reporte.clicked.connect(self.descargar_pdf)
        self._main_window = parent  # Para volver al main

    def set_datos(self, datos):
        # datos: dict con keys: fecha, localidad, chofer, vehiculo, cliente, total, productos (lista de dicts)
        self.label_fecha_reporte.setText(datos['fecha'])
        self.label_localidad_reporte.setText(datos['localidad'])
        self.label_chofer_reporte.setText(datos['chofer'])
        self.label_vehiculo_reporte.setText(datos['vehiculo'])
        self.label_cliente_reporte.setText(datos['cliente'])
        self.label_total_reporte.setText(str(datos['total']))
        # Llenar tabla productos
        self.tabla_productos_report.setRowCount(0)
        for prod in datos['productos']:
            row = self.tabla_productos_report.rowCount()
            self.tabla_productos_report.insertRow(row)
            self.tabla_productos_report.setItem(row, 0, QTableWidgetItem(str(prod['detalle'])))
            self.tabla_productos_report.setItem(row, 1, QTableWidgetItem(str(prod['precio'])))
            self.tabla_productos_report.setItem(row, 2, QTableWidgetItem(str(prod['cantidad'])))
            self.tabla_productos_report.setItem(row, 3, QTableWidgetItem(str(prod['subtotal'])))

    def volver(self):
        if self._main_window:
            self.hide()
            self._main_window.show()

    def descargar_pdf(self):
        # Guardar screenshot del frame como imagen en la carpeta planillas
        carpeta = os.path.join(os.getcwd(), 'planillas')
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        nombre = QFileDialog.getSaveFileName(self, "Guardar reporte", carpeta, "Imagen PNG (*.png)")[0]
        if not nombre:
            return
        if not nombre.lower().endswith('.png'):
            nombre += '.png'
        # Usar el nombre correcto del frame según el .ui
        pixmap = QPixmap(self.frame_reporte.size())
        self.frame_reporte.render(pixmap)
        pixmap.save(nombre, 'PNG')
