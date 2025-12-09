from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QTableWidgetItem, QFrame
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi


import sys
from system.localidad.localidad import Localidad
from system.producto.producto import Producto
from system.chofer.chofer import Chofer
from system.vehiculo.vehiculo import Vehiculo
from system.cliente.cliente import Cliente

class Main(QMainWindow):
    def __init__(self, parent=None):

        super(Main, self).__init__(parent)
        loadUi('pantallas.ui', self)
        # Asignar la fecha actual al campo de la planilla
        from PyQt5.QtCore import QDate
        hoy = QDate.currentDate().toString("dd/MM/yyyy")
        if hasattr(self, "lineEdit_fecha"):
            self.lineEdit_fecha.setText(hoy)
        # Configuración de botones de planilla
        import sqlite3
        self.tabla_seleccionar_datos = self.findChild(QTableWidget, "tabla_seleccionar_datos")
        self.btn_agregar_localidad_planilla = self.findChild(QPushButton, "btn_agregar_localidad_planilla")
        self.btn_agregar_producto_planilla = self.findChild(QPushButton, "btn_agregar_producto_planilla")
        self.btn_agregar_chofer_planilla = self.findChild(QPushButton, "btn_agregar_chofer_planilla")
        self.btn_agregar_vehiculo_planilla = self.findChild(QPushButton, "btn_agregar_vehiculo_planilla")
        self.btn_agregar_cliente_planilla = self.findChild(QPushButton, "btn_agregar_cliente_planilla")
        self.btn_agregar_planilla_2 = self.findChild(QPushButton, "btn_agregar_planilla_2")
        self.frame_6 = self.findChild(QFrame, "frame_6")
        self.frame_10 = self.findChild(QFrame, "frame_10")
        # Ocultar los frames al inicio
        if self.frame_6:
            self.frame_6.setVisible(False)
        if self.frame_10:
            self.frame_10.setVisible(False)
        self.btn_agregar_localidad_planilla.clicked.connect(self.mostrar_localidades)
        self.btn_agregar_producto_planilla.clicked.connect(self.mostrar_productos)
        self.btn_agregar_chofer_planilla.clicked.connect(self.mostrar_choferes)
        self.btn_agregar_vehiculo_planilla.clicked.connect(self.mostrar_vehiculos)
        self.btn_agregar_cliente_planilla.clicked.connect(self.mostrar_clientes)
        # Mostrar frames al presionar btn_agregar_planilla_2
        if self.btn_agregar_planilla_2:
            self.btn_agregar_planilla_2.clicked.connect(self.mostrar_frames_planilla)
        # defino las variables que voy a utilizar
        self.lastId=0
        self.selectedId=0
        self.filaTabla=0
        self.estado='CONSULTAR'   

        #------------- LOCALIDADES
        Localidad.showLocalidades(self) #primero muestro contenidos en la pantalla
        Localidad.readLocalidades(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarLocalidad.clicked.connect(lambda: Localidad.saveLocalidades(self))

        self.btnAgregarLocalidad.clicked.connect(lambda: Localidad.createLocalidades(self))
        self.btnEditarLocalidad.clicked.connect(lambda: Localidad.updateLocalidades(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarLocalidad.clicked.connect(lambda: Localidad.searchLocalidades(self))

        self.tablalocalidad.doubleClicked.connect(lambda: Localidad.doubleClicked_tabla(self))    
        self.tablalocalidad.clicked.connect(lambda: Localidad.clicked_tabla(self))

#------------- PRODUCTOS
        Producto.showProductos(self) #primero muestro contenidos en la pantalla
        Producto.readProductos(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarProducto.clicked.connect(lambda: Producto.saveProductos(self))

        self.btnAgregarProducto.clicked.connect(lambda: Producto.createProductos(self))
        self.btnEditarProducto.clicked.connect(lambda: Producto.updateProductos(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarProducto.clicked.connect(lambda: Producto.searchProductos(self))

        self.tablaproductos.doubleClicked.connect(lambda: Producto.doubleClicked_tabla(self))    
        self.tablaproductos.clicked.connect(lambda: Producto.clicked_tabla(self))

#------------- CHOFERES
        Chofer.showChoferes(self) #primero muestro contenidos en la pantalla  
        Chofer.readChoferes(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarChofer.clicked.connect(lambda: Chofer.saveChoferes(self))

        self.btnAgregarChofer.clicked.connect(lambda: Chofer.createChoferes(self))
        self.btnEditarChofer.clicked.connect(lambda: Chofer.updateChoferes(self))
        self.btnEliminarChofer.clicked.connect(lambda: Chofer.deleteChoferes(self))
        self.btnBuscarChofer.clicked.connect(lambda: Chofer.searchChoferes(self))
        self.tablachoferes.doubleClicked.connect(lambda: Chofer.doubleClicked_tabla(self))    
        self.tablachoferes.clicked.connect(lambda: Chofer.clicked_tabla(self))

#------------- VEHICULOS
        self.vehiculo = Vehiculo()
        self.vehiculo.showVehiculos(self)
        self.btn_guardar_vehiculo.clicked.connect(lambda: self.vehiculo.saveVehiculos(self))
        self.btn_agregar_vehiculo.clicked.connect(lambda: self.vehiculo.createVehiculos(self))
        self.btn_editar_vehiculo.clicked.connect(lambda: self.vehiculo.updateVehiculos(self))
        self.btn_eliminar_vehiculo.clicked.connect(lambda: self.vehiculo.deleteVehiculos(self))
        self.btn_buscar_vehiculo.clicked.connect(lambda: self.vehiculo.searchVehiculos(self))
        self.tablavehiculo.doubleClicked.connect(lambda: self.vehiculo.doubleClicked_tabla(self))
        self.tablavehiculo.clicked.connect(lambda: self.vehiculo.clicked_tabla(self))
        # El lineEdit_buscar_2 se usa para escribir el texto a filtrar en la búsqueda de vehículos.

#------------- CLIENTES
        self.cliente = Cliente()
        self.cliente.showClientes(self)
        self.btn_guardar_cliente.clicked.connect(lambda: self.cliente.saveClientes(self))
        self.btn_agregar_cliente.clicked.connect(lambda: self.cliente.createClientes(self))
        if hasattr(self, 'btn_agregar_cliente_3'):
            self.btn_agregar_cliente_3.clicked.connect(lambda: self.cliente.createClientes(self))
        self.btn_editar_cliente.clicked.connect(lambda: self.cliente.updateClientes(self))
        self.btn_eliminar_cliente.clicked.connect(lambda: self.cliente.deleteClientes(self))
        self.btn_buscar_cliente.clicked.connect(lambda: self.cliente.searchClientes(self))
        self.tabla_cliente.doubleClicked.connect(lambda: self.cliente.doubleClicked_tabla(self) if hasattr(self.cliente, 'doubleClicked_tabla') else None)
        self.tabla_cliente.clicked.connect(lambda: self.cliente.clicked_tabla(self) if hasattr(self.cliente, 'clicked_tabla') else None)
        # El lineEdit_buscar_cliente se usa para escribir el texto a filtrar en la búsqueda de clientes.

    def cargar_tabla(self, query, headers):
        import sqlite3
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
                self.tabla_seleccionar_datos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
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

    def mostrar_frames_planilla(self):
        if self.frame_6:
            self.frame_6.setVisible(True)
        if self.frame_10:
            self.frame_10.setVisible(True)

# ------ main -------------
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Main()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())