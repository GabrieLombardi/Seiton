
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QTableWidgetItem, QFrame, QInputDialog, QMessageBox, QLabel
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate

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
        hoy = QDate.currentDate().toString("dd/MM/yyyy")
        if hasattr(self, "lineEdit_fecha"):
            self.lineEdit_fecha.setText(hoy)
        # Inicializar el label_cod_planilla con el próximo número
        self.label_cod_planilla = self.findChild(QLabel, "label_cod_planilla")
        self.actualizar_label_cod_planilla()
        # Llenar la tabla de planillas al iniciar
        self.mostrar_planillas()
        # Configuración de botones de planilla
        import sqlite3
        self.tabla_seleccionar_datos = self.findChild(QTableWidget, "tabla_seleccionar_datos")
        # Ocultar la columna ID en la tabla de selección (siempre la primera)
        self.tabla_seleccionar_datos.setColumnHidden(0, True)
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
        self.lastId = 0
        self.selectedId = 0
        self.filaTabla = 0
        self.estado = 'CONSULTAR'

        # ------------- LOCALIDADES
        Localidad.showLocalidades(self)  # primero muestro contenidos en la pantalla
        Localidad.readLocalidades(self, self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarLocalidad.clicked.connect(lambda: Localidad.saveLocalidades(self))
        self.btnAgregarLocalidad.clicked.connect(lambda: Localidad.createLocalidades(self))
        self.btnEditarLocalidad.clicked.connect(lambda: Localidad.updateLocalidades(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarLocalidad.clicked.connect(lambda: Localidad.searchLocalidades(self))
        self.tablalocalidad.doubleClicked.connect(lambda: Localidad.doubleClicked_tabla(self))
        self.tablalocalidad.clicked.connect(lambda: Localidad.clicked_tabla(self))

        # ------------- PRODUCTOS
        Producto.showProductos(self)  # primero muestro contenidos en la pantalla
        Producto.readProductos(self, self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarProducto.clicked.connect(lambda: Producto.saveProductos(self))
        self.btnAgregarProducto.clicked.connect(lambda: Producto.createProductos(self))
        self.btnEditarProducto.clicked.connect(lambda: Producto.updateProductos(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarProducto.clicked.connect(lambda: Producto.searchProductos(self))
        self.tablaproductos.doubleClicked.connect(lambda: Producto.doubleClicked_tabla(self))
        self.tablaproductos.clicked.connect(lambda: Producto.clicked_tabla(self))

        # ------------- CHOFERES
        Chofer.showChoferes(self)  # primero muestro contenidos en la pantalla
        Chofer.readChoferes(self, self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarChofer.clicked.connect(lambda: Chofer.saveChoferes(self))
        self.btnAgregarChofer.clicked.connect(lambda: Chofer.createChoferes(self))
        self.btnEditarChofer.clicked.connect(lambda: Chofer.updateChoferes(self))
        self.btnEliminarChofer.clicked.connect(lambda: Chofer.deleteChoferes(self))
        self.btnBuscarChofer.clicked.connect(lambda: Chofer.searchChoferes(self))
        self.tablachoferes.doubleClicked.connect(lambda: Chofer.doubleClicked_tabla(self))
        self.tablachoferes.clicked.connect(lambda: Chofer.clicked_tabla(self))

        # ------------- VEHICULOS
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

        # ------------- CLIENTES
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

        self.ultima_entidad = None
        self.cliente_seleccionado = None
        self.localidad_seleccionada = None
        self.chofer_seleccionado = None
        self.vehiculo_seleccionado = None
        self.id_cliente_seleccionado = None
        self.id_localidad_seleccionada = None
        self.id_chofer_seleccionado = None
        self.id_vehiculo_seleccionado = None
        # Conexión de botones para seleccionar entidad
        self.btn_agregar_localidad_planilla.clicked.connect(lambda: self.set_entidad('localidad'))
        self.btn_agregar_producto_planilla.clicked.connect(lambda: self.set_entidad('producto'))
        self.btn_agregar_chofer_planilla.clicked.connect(lambda: self.set_entidad('chofer'))
        self.btn_agregar_vehiculo_planilla.clicked.connect(lambda: self.set_entidad('vehiculo'))
        self.btn_agregar_cliente_planilla.clicked.connect(lambda: self.set_entidad('cliente'))
        # Eliminar conexión innecesaria:
        # self.btn_buscar_3.clicked.connect(self.buscar_en_tabla_seleccionar)
        self.btn_agregar_a_planilla.clicked.connect(self.agregar_a_resumen)

        self.tabla_resumen_productos = self.findChild(QTableWidget, "tabla_resumen_productos")
        # Inicializar tabla_resumen_productos con 0 filas y 4 columnas
        self.tabla_resumen_productos.setColumnCount(5)
        self.tabla_resumen_productos.setHorizontalHeaderLabels(["ID", "Detalle", "Precio", "Cantidad", "Subtotal"])
        self.tabla_resumen_productos.setColumnHidden(0, True)
        if hasattr(self, 'btn_continuar_planilla'):
            self.btn_continuar_planilla.clicked.connect(self.guardar_planilla)

    def actualizar_label_cod_planilla(self):
        import sqlite3
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(nro_planilla) FROM planilla")
        res = cursor.fetchone()
        nro = (res[0] or 0) + 1
        texto = str(nro).zfill(2)
        if self.label_cod_planilla:
            self.label_cod_planilla.setText(texto)
        conn.close()

    def mostrar_planillas(self):
        import sqlite3
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        query = '''
            SELECT p.nro_planilla, p.fecha,
                   COALESCE(c.nombre, 'Sin asignar') AS cliente,
                   COALESCE(ch.Nombre, 'Sin asignar') AS chofer,
                   COALESCE(l.nombreloc, 'Sin asignar') AS localidad,
                   p.total
            FROM planilla p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
            LEFT JOIN chofer ch ON p.id_chofer = ch.id_chofer
            LEFT JOIN localidad l ON p.id_localidad = l.Id_localidad
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = ["Nro Planilla", "Fecha", "Cliente", "Chofer", "Localidad", "Total"]
        self.tabla_planillas = self.findChild(QTableWidget, "tabla_planillas")
        self.tabla_planillas.setRowCount(len(rows))
        self.tabla_planillas.setColumnCount(len(headers))
        self.tabla_planillas.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.tabla_planillas.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        conn.close()

    def guardar_planilla(self):
        import sqlite3
        id_cliente = self.id_cliente_seleccionado if hasattr(self, 'id_cliente_seleccionado') else None
        id_chofer = self.id_chofer_seleccionado if hasattr(self, 'id_chofer_seleccionado') else None
        id_localidad = self.id_localidad_seleccionada if hasattr(self, 'id_localidad_seleccionada') else None
        id_vehiculo = self.id_vehiculo_seleccionado if hasattr(self, 'id_vehiculo_seleccionado') else None
        fecha = QDate.currentDate().toString("dd/MM/yyyy")
        total = self.lineEdit_total.text() if hasattr(self, 'lineEdit_total') else "0"
        nro_planilla = int(self.label_cod_planilla.text()) if self.label_cod_planilla else None
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO planilla (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total)
        )
        conn.commit()
        id_planilla = cursor.lastrowid
        for i in range(self.tabla_resumen_productos.rowCount()):
            detalle = self.tabla_resumen_productos.item(i, 0).text() if self.tabla_resumen_productos.item(i, 0) else ""
            cantidad = self.tabla_resumen_productos.item(i, 2).text() if self.tabla_resumen_productos.item(i, 2) else "0"
            subtotal = self.tabla_resumen_productos.item(i, 3).text() if self.tabla_resumen_productos.item(i, 3) else "0"
            cursor.execute("SELECT id_producto FROM Producto WHERE descripcion = ?", (detalle,))
            res = cursor.fetchone()
            id_producto = res[0] if res else None
            cursor.execute(
                "INSERT INTO productoxplanilla (id_planilla, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                (id_planilla, id_producto, cantidad, subtotal)
            )
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Guardado", "La planilla y los productos fueron guardados correctamente.")
        # Actualizar el label para el próximo número
        self.actualizar_label_cod_planilla()

    def cargar_tabla(self, query, headers):
        import sqlite3
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        # Ahora la columna ID siempre se muestra y es la primera
        self.tabla_seleccionar_datos.setRowCount(len(rows))
        self.tabla_seleccionar_datos.setColumnCount(len(headers))
        self.tabla_seleccionar_datos.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.tabla_seleccionar_datos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        conn.close()
        # Ocultar la columna ID si existe
        if self.tabla_seleccionar_datos.columnCount() > 0:
            self.tabla_seleccionar_datos.setColumnHidden(0, True)

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

    def set_entidad(self, entidad):
        self.ultima_entidad = entidad

    def actualizar_total_productos(self):
        total = 0.0
        for i in range(self.tabla_resumen_productos.rowCount()):
            item = self.tabla_resumen_productos.item(i, 4)  # Columna 4 es el subtotal
            if item:
                try:
                    total += float(item.text())
                except ValueError:
                    pass
        if hasattr(self, 'lineEdit_total'):
            self.lineEdit_total.setText(f"{total:.2f}")

    def agregar_a_resumen(self):
        row = self.tabla_seleccionar_datos.currentRow()
        if row == -1 or not self.ultima_entidad:
            return
        # Detectar índice según headers
        def get_index(header_name):
            headers = [self.tabla_seleccionar_datos.horizontalHeaderItem(j).text() for j in range(self.tabla_seleccionar_datos.columnCount())]
            try:
                return headers.index(header_name)
            except ValueError:
                return None
        datos = [self.tabla_seleccionar_datos.item(row, col).text() if self.tabla_seleccionar_datos.item(row, col) else "" for col in range(self.tabla_seleccionar_datos.columnCount())]
        if self.ultima_entidad == 'producto':
            idx_detalle = get_index('Descripción')
            idx_precio = get_index('Precio')
            if idx_detalle is None or idx_precio is None:
                QMessageBox.warning(self, "Error", "No se pudo obtener el detalle o precio del producto.")
                return
            detalle = datos[idx_detalle]
            try:
                precio = float(datos[idx_precio])
            except ValueError:
                QMessageBox.warning(self, "Error", "El precio no es válido.")
                return
            cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"Ingrese la cantidad para '{detalle}':", 1, 1)
            if not ok:
                return
            subtotal = precio * cantidad
            # Buscar el ID del producto por la descripción
            import sqlite3
            conn = sqlite3.connect('pedidos.sqlite3')
            cursor = conn.cursor()
            cursor.execute("SELECT id_producto FROM Producto WHERE descripcion = ?", (detalle,))
            res = cursor.fetchone()
            id_producto = res[0] if res else None
            conn.close()
            # Buscar si el producto ya existe en la tabla (por ID)
            row_found = None
            for i in range(self.tabla_resumen_productos.rowCount()):
                if self.tabla_resumen_productos.item(i, 0) and self.tabla_resumen_productos.item(i, 0).text() == str(id_producto):
                    row_found = i
                    break
            if row_found is not None:
                cantidad_actual = int(self.tabla_resumen_productos.item(row_found, 3).text())
                subtotal_actual = float(self.tabla_resumen_productos.item(row_found, 4).text())
                nueva_cantidad = cantidad_actual + cantidad
                nuevo_subtotal = subtotal_actual + subtotal
                self.tabla_resumen_productos.setItem(row_found, 3, QTableWidgetItem(str(nueva_cantidad)))
                self.tabla_resumen_productos.setItem(row_found, 4, QTableWidgetItem(f"{nuevo_subtotal:.2f}"))
            else:
                row_pos = self.tabla_resumen_productos.rowCount()
                self.tabla_resumen_productos.insertRow(row_pos)
                self.tabla_resumen_productos.setItem(row_pos, 0, QTableWidgetItem(str(id_producto) if id_producto else ""))
                self.tabla_resumen_productos.setItem(row_pos, 1, QTableWidgetItem(detalle))
                self.tabla_resumen_productos.setItem(row_pos, 2, QTableWidgetItem(f"{precio:.2f}"))
                self.tabla_resumen_productos.setItem(row_pos, 3, QTableWidgetItem(str(cantidad)))
                self.tabla_resumen_productos.setItem(row_pos, 4, QTableWidgetItem(f"{subtotal:.2f}"))
            self.actualizar_total_productos()
            return
            self.actualizar_total_productos()
            return
        # Guardar la fila completa y el ID real (primer campo) para cada entidad
        if self.ultima_entidad == 'cliente':
            self.cliente_seleccionado = datos if datos else None
            self.id_cliente_seleccionado = datos[0] if datos else None
        elif self.ultima_entidad == 'localidad':
            self.localidad_seleccionada = datos if datos else None
            self.id_localidad_seleccionada = datos[0] if datos else None
        elif self.ultima_entidad == 'chofer':
            self.chofer_seleccionado = datos if datos else None
            self.id_chofer_seleccionado = datos[0] if datos else None
        elif self.ultima_entidad == 'vehiculo':
            self.vehiculo_seleccionado = datos if datos else None
            self.id_vehiculo_seleccionado = datos[0] if datos else None
        self.actualizar_tabla_resumen()

    def actualizar_tabla_resumen(self):
        nombres = ["Cliente", "Localidad", "Chofer", "Vehiculo"]
        # Solo inicializar la tabla una vez si está vacía
        if self.tabla_resumen.rowCount() != 4 or self.tabla_resumen.columnCount() != 2:
            self.tabla_resumen.setRowCount(4)
            self.tabla_resumen.setColumnCount(2)
            self.tabla_resumen.setHorizontalHeaderLabels(["Entidad", "Detalle"])
            for i, nombre in enumerate(nombres):
                self.tabla_resumen.setItem(i, 0, QTableWidgetItem(nombre))
        # Cliente
        if self.cliente_seleccionado:
            idx = self._get_index('Nombre', self.cliente_seleccionado)
            if idx is not None:
                self.tabla_resumen.setItem(0, 1, QTableWidgetItem(self.cliente_seleccionado[idx]))
        # Localidad
        if self.localidad_seleccionada:
            idx = self._get_index('nombreloc', self.localidad_seleccionada)
            if idx is None:
                idx = self._get_index('Nombre', self.localidad_seleccionada)
            if idx is not None:
                self.tabla_resumen.setItem(1, 1, QTableWidgetItem(self.localidad_seleccionada[idx]))
        # Chofer
        if self.chofer_seleccionado:
            idx = self._get_index('Nombre', self.chofer_seleccionado)
            if idx is not None:
                self.tabla_resumen.setItem(2, 1, QTableWidgetItem(self.chofer_seleccionado[idx]))
        # Vehiculo
        if self.vehiculo_seleccionado:
            idx = self._get_index('Descripción', self.vehiculo_seleccionado)
            if idx is not None:
                self.tabla_resumen.setItem(3, 1, QTableWidgetItem(self.vehiculo_seleccionado[idx]))

    def _get_index(self, header_name, datos):
        headers = [self.tabla_seleccionar_datos.horizontalHeaderItem(j).text() for j in range(self.tabla_seleccionar_datos.columnCount())]
        try:
            return headers.index(header_name)
        except ValueError:
            return None

    def guardar_planilla(self):
        import sqlite3
        # Asegurarse que los IDs sean enteros
        try:
            id_cliente = int(self.id_cliente_seleccionado)
        except (TypeError, ValueError):
            id_cliente = None
        try:
            id_chofer = int(self.id_chofer_seleccionado)
        except (TypeError, ValueError):
            id_chofer = None
        try:
            id_localidad = int(self.id_localidad_seleccionada)
        except (TypeError, ValueError):
            id_localidad = None
        try:
            id_vehiculo = int(self.id_vehiculo_seleccionado)
        except (TypeError, ValueError):
            id_vehiculo = None
        fecha = QDate.currentDate().toString("dd/MM/yyyy")
        total = self.lineEdit_total.text() if hasattr(self, 'lineEdit_total') else "0"
        nro_planilla = int(self.label_cod_planilla.text()) if self.label_cod_planilla else None
        # Validar que todas las entidades estén seleccionadas
        if not all([id_cliente, id_chofer, id_localidad, id_vehiculo]):
            QMessageBox.warning(self, "Faltan datos", "Debe seleccionar cliente, chofer, localidad y vehículo antes de guardar.")
            return
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO planilla (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total)
        )
        conn.commit()
        id_planilla = cursor.lastrowid
        for i in range(self.tabla_resumen_productos.rowCount()):
            # Siempre usar el ID de la columna 0
            try:
                id_producto = int(self.tabla_resumen_productos.item(i, 0).text()) if self.tabla_resumen_productos.item(i, 0) else None
            except (TypeError, ValueError):
                id_producto = None
            cantidad = self.tabla_resumen_productos.item(i, 3).text() if self.tabla_resumen_productos.item(i, 3) else "0"
            subtotal = self.tabla_resumen_productos.item(i, 4).text() if self.tabla_resumen_productos.item(i, 4) else "0"
            if id_producto:
                cursor.execute(
                    "INSERT INTO productoxplanilla (id_planilla, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                    (id_planilla, id_producto, cantidad, subtotal)
                )
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Guardado", "La planilla y los productos fueron guardados correctamente.")

# ------ main -------------
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Main()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())