from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
import sqlite3

class PlanillaWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("pantallas.ui", self)
        hoy = QDate.currentDate().toString("dd/MM/yyyy")
        if hasattr(self, "lineEdit_fecha"):
            self.lineEdit_fecha.setText(hoy)
        # Obtener widgets por name si no están como atributos
        self.tabla_seleccionar_datos = self.findChild(QtWidgets.QTableWidget, "tabla_seleccionar_datos")
        self.btn_agregar_localidad_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_localidad_planilla")
        self.btn_agregar_producto_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_producto_planilla")
        self.btn_agregar_chofer_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_chofer_planilla")
        self.btn_agregar_vehiculo_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_vehiculo_planilla")
        self.btn_agregar_cliente_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_cliente_planilla")
        self.btn_agregar_a_planilla = self.findChild(QtWidgets.QPushButton, "btn_agregar_a_planilla")
        self.tabla_resumen = self.findChild(QtWidgets.QTableWidget, "tabla_resumen")
        # Conexión de botones para filtrar y mostrar datos en tabla_seleccionar_datos
        self.btn_agregar_localidad_planilla.clicked.connect(lambda: self.seleccionar_entidad('localidad'))
        self.btn_agregar_producto_planilla.clicked.connect(lambda: self.seleccionar_entidad('producto'))
        self.btn_agregar_chofer_planilla.clicked.connect(lambda: self.seleccionar_entidad('chofer'))
        self.btn_agregar_vehiculo_planilla.clicked.connect(lambda: self.seleccionar_entidad('vehiculo'))
        self.btn_agregar_cliente_planilla.clicked.connect(lambda: self.seleccionar_entidad('cliente'))

    def seleccionar_entidad(self, entidad):
        self.ultima_entidad = entidad
        if entidad == 'localidad':
            self.mostrar_localidades()
        elif entidad == 'producto':
            self.mostrar_productos()
        elif entidad == 'chofer':
            self.mostrar_choferes()
        elif entidad == 'vehiculo':
            self.mostrar_vehiculos()
        elif entidad == 'cliente':
            self.mostrar_clientes()

    def cargar_tabla(self, query, headers):
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        # Omitir la columna ID
        if headers and headers[0].strip().upper() == 'ID':
            headers = headers[1:]
            rows = [row[1:] for row in rows]
        self.tabla_seleccionar_datos.setRowCount(len(rows))
        self.tabla_seleccionar_datos.setColumnCount(len(headers))
        self.tabla_seleccionar_datos.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.tabla_seleccionar_datos.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        conn.close()

    def mostrar_localidades(self):
        query = "SELECT * FROM localidad"
        headers = ['ID', 'Nombre', 'Código Postal']
        self.cargar_tabla(query, headers)

    def mostrar_productos(self):
        query = "SELECT * FROM Producto"
        headers = ['ID', 'Descripción', 'Código', 'Precio']
        self.cargar_tabla(query, headers)

    def mostrar_choferes(self):
        query = "SELECT * FROM chofer"
        headers = ['ID', 'Nombre', 'Cuit', 'DNI', 'F/Nac', 'Teléfono', 'Dirección']
        self.cargar_tabla(query, headers)

    def mostrar_vehiculos(self):
        query = "SELECT * FROM vehiculo"
        headers = ['ID', 'Matricula', 'Descripción']
        self.cargar_tabla(query, headers)

    def mostrar_clientes(self):
        query = "SELECT c.id_cliente, c.nombre, c.cuit, c.direccion, c.tel, c.dni, l.nombreloc FROM cliente c LEFT JOIN localidad l ON c.id_loc = l.Id_localidad"
        headers = ['ID', 'Nombre', 'Cuit', 'Dirección', 'Teléfono', 'DNI', 'Localidad']
        self.cargar_tabla(query, headers)

    def set_entidad(self, entidad):
        self.ultima_entidad = entidad

    def agregar_a_resumen(self):
        row = self.tabla_seleccionar_datos.currentRow()
        if row == -1 or not self.ultima_entidad:
            return
        # Guardar el ID real y mostrar el nombre en la tabla resumen
        if self.ultima_entidad == 'cliente':
            id_item = self.tabla_seleccionar_datos.item(row, 0)
            nombre_item = self.tabla_seleccionar_datos.item(row, 1)
            self.id_cliente_seleccionado = id_item.text() if id_item else None
            nombre = nombre_item.text() if nombre_item else ""
            self.tabla_resumen.setItem(0, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'localidad':
            id_item = self.tabla_seleccionar_datos.item(row, 0)
            nombre_item = self.tabla_seleccionar_datos.item(row, 1)
            self.id_localidad_seleccionada = id_item.text() if id_item else None
            nombre = nombre_item.text() if nombre_item else ""
            self.tabla_resumen.setItem(1, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'chofer':
            id_item = self.tabla_seleccionar_datos.item(row, 0)
            nombre_item = self.tabla_seleccionar_datos.item(row, 1)
            self.id_chofer_seleccionado = id_item.text() if id_item else None
            nombre = nombre_item.text() if nombre_item else ""
            self.tabla_resumen.setItem(2, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'vehiculo':
            id_item = self.tabla_seleccionar_datos.item(row, 0)
            nombre_item = self.tabla_seleccionar_datos.item(row, 1)
            self.id_vehiculo_seleccionado = id_item.text() if id_item else None
            nombre = nombre_item.text() if nombre_item else ""
            self.tabla_resumen.setItem(3, 1, QtWidgets.QTableWidgetItem(str(nombre)))

    def showEvent(self, event):
        super().showEvent(event)
        # Forzar encabezados verticales cada vez que se muestra la ventana
        self.tabla_resumen.setVerticalHeaderLabels(["Cliente", "Localidad", "Chofer", "Vehiculo"])
