from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate
import sqlite3

class PlanillaWindow(QtWidgets.QWidget):
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
        self.btn_agregar_localidad_planilla.clicked.connect(self.mostrar_localidades)
        self.btn_agregar_producto_planilla.clicked.connect(self.mostrar_productos)
        self.btn_agregar_chofer_planilla.clicked.connect(self.mostrar_choferes)
        self.btn_agregar_vehiculo_planilla.clicked.connect(self.mostrar_vehiculos)
        self.btn_agregar_cliente_planilla.clicked.connect(self.mostrar_clientes)
        if self.btn_agregar_a_planilla:
            self.btn_agregar_a_planilla.clicked.connect(self.agregar_a_resumen)

        self.ultima_entidad = None
        self.cliente_seleccionado = None
        self.localidad_seleccionada = None
        self.chofer_seleccionado = None
        self.vehiculo_seleccionado = None

        # Inicializar tabla_resumen con 4 filas y 1 columna
        self.tabla_resumen.setRowCount(4)
        self.tabla_resumen.setColumnCount(2)
        self.tabla_resumen.setHorizontalHeaderLabels(["Entidad", "Detalle"])
        nombres = ["Cliente", "Localidad", "Chofer", "Vehiculo"]
        for i, nombre in enumerate(nombres):
            self.tabla_resumen.setItem(i, 0, QtWidgets.QTableWidgetItem(nombre))
            self.tabla_resumen.setItem(i, 1, QtWidgets.QTableWidgetItem(""))

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
        # Solo copiar el campo específico (nombre) de cada entidad
        if self.ultima_entidad == 'cliente':
            indice_nombre = 1  # columna del nombre en tabla_seleccionar_datos
            item = self.tabla_seleccionar_datos.item(row, indice_nombre)
            nombre = item.text() if item else ""
            self.tabla_resumen.setItem(0, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'localidad':
            indice_nombre = 1
            item = self.tabla_seleccionar_datos.item(row, indice_nombre)
            nombre = item.text() if item else ""
            self.tabla_resumen.setItem(1, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'chofer':
            indice_nombre = 1
            item = self.tabla_seleccionar_datos.item(row, indice_nombre)
            nombre = item.text() if item else ""
            self.tabla_resumen.setItem(2, 1, QtWidgets.QTableWidgetItem(str(nombre)))
        elif self.ultima_entidad == 'vehiculo':
            indice_nombre = 1
            item = self.tabla_seleccionar_datos.item(row, indice_nombre)
            nombre = item.text() if item else ""
            self.tabla_resumen.setItem(3, 1, QtWidgets.QTableWidgetItem(str(nombre)))

    def showEvent(self, event):
        super().showEvent(event)
        # Forzar encabezados verticales cada vez que se muestra la ventana
        self.tabla_resumen.setVerticalHeaderLabels(["Cliente", "Localidad", "Chofer", "Vehiculo"])


