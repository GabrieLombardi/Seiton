
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

        # Referencias a los nuevos widgets del reporte
        self.frame_reporte = self.findChild(QFrame, "frame_reporte")
        self.label_fecha_reporte = self.findChild(QLabel, "label_fecha_reporte")
        self.label_localidad_reporte = self.findChild(QLabel, "label_localidad_reporte")
        self.label_chofer_reporte = self.findChild(QLabel, "label_chofer_reporte")
        self.label_vehiculo_reporte = self.findChild(QLabel, "label_vehiculo_reporte")
        self.label_cliente_reporte = self.findChild(QLabel, "label_cliente_reporte")
        self.label_total_reporte = self.findChild(QLabel, "label_total_reporte")
        self.tabla_productos_reporte = self.findChild(QTableWidget, "tabla_productos_reporte")
        self.btn_volver_reporte = self.findChild(QPushButton, "btn_volver_reporte")
        self.btn_descargar_reporte = self.findChild(QPushButton, "btn_descargar_reporte")

        # Ocultar el frame de reporte al inicio
        if self.frame_reporte:
            self.frame_reporte.setVisible(False)
        if self.btn_volver_reporte:
            self.btn_volver_reporte.clicked.connect(self.volver_de_reporte)
        if self.btn_descargar_reporte:
            self.btn_descargar_reporte.clicked.connect(self.descargar_reporte_imagen)

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
        # Validar que todos los IDs estén seleccionados
        id_cliente = self.id_cliente_seleccionado if hasattr(self, 'id_cliente_seleccionado') else None
        id_chofer = self.id_chofer_seleccionado if hasattr(self, 'id_chofer_seleccionado') else None
        id_localidad = self.id_localidad_seleccionada if hasattr(self, 'id_localidad_seleccionada') else None
        id_vehiculo = self.id_vehiculo_seleccionado if hasattr(self, 'id_vehiculo_seleccionado') else None
        if not all([id_cliente, id_chofer, id_localidad, id_vehiculo]):
            QMessageBox.warning(self, "Faltan datos", "Debe seleccionar cliente, chofer, localidad y vehículo antes de continuar.")
            return
        if self.tabla_resumen_productos.rowCount() == 0:
            QMessageBox.warning(self, "Faltan productos", "Debe agregar al menos un producto a la planilla.")
            return
        fecha = QDate.currentDate().toString("dd/MM/yyyy")
        total = self.lineEdit_total.text() if hasattr(self, 'lineEdit_total') else "0"
        nro_planilla = int(self.label_cod_planilla.text()) if self.label_cod_planilla else None
        try:
            conn = sqlite3.connect('pedidos.sqlite3')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO planilla (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nro_planilla, fecha, id_cliente, id_chofer, id_localidad, id_vehiculo, total)
            )
            conn.commit()
            id_planilla = cursor.lastrowid
            for i in range(self.tabla_resumen_productos.rowCount()):
                id_producto = self.tabla_resumen_productos.item(i, 0).text() if self.tabla_resumen_productos.item(i, 0) else ""
                cantidad = self.tabla_resumen_productos.item(i, 3).text() if self.tabla_resumen_productos.item(i, 3) else "0"
                subtotal = self.tabla_resumen_productos.item(i, 4).text() if self.tabla_resumen_productos.item(i, 4) else "0"
                if not id_producto:
                    QMessageBox.warning(self, "Error de producto", f"No se encontró el ID de producto en la fila {i+1}.")
                    continue
                cursor.execute(
                    "INSERT INTO productoxplanilla (id_planilla, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                    (id_planilla, id_producto, cantidad, subtotal)
                )
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", f"Ocurrió un error al guardar la planilla: {str(e)}")
            return
        # Mostrar el reporte con los datos del último registro
        try:
            conn = sqlite3.connect('pedidos.sqlite3')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.fecha, l.nombreloc, ch.Nombre, v.descripcion, c.nombre, p.total, p.nro_planilla
                FROM planilla p
                LEFT JOIN localidad l ON p.id_localidad = l.Id_localidad
                LEFT JOIN chofer ch ON p.id_chofer = ch.id_chofer
                LEFT JOIN vehiculo v ON p.id_vehiculo = v.id_vehiculo
                LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
                WHERE p.nro_planilla = ?
            ''', (nro_planilla,))
            row = cursor.fetchone()
            if not row:
                QMessageBox.critical(self, "Error", "No se pudo recuperar la planilla recién guardada.")
                return
            # Llenar los labels del reporte
            if self.label_fecha_reporte: self.label_fecha_reporte.setText(str(row[0]))
            if self.label_localidad_reporte: self.label_localidad_reporte.setText(str(row[1]))
            if self.label_chofer_reporte: self.label_chofer_reporte.setText(str(row[2]))
            if self.label_vehiculo_reporte: self.label_vehiculo_reporte.setText(str(row[3]))
            if self.label_cliente_reporte: self.label_cliente_reporte.setText(str(row[4]))
            if self.label_total_reporte: self.label_total_reporte.setText(str(row[5]))
            # Llenar la tabla de productos del reporte
            if self.tabla_productos_reporte:
                self.tabla_productos_reporte.setRowCount(0)
                cursor.execute('''
                    SELECT pr.descripcion, pr.precio_unid, pxp.cantidad, pxp.subtotal
                    FROM productoxplanilla pxp
                    JOIN Producto pr ON pxp.id_producto = pr.id_producto
                    WHERE pxp.id_planilla = (SELECT id_planilla FROM planilla WHERE nro_planilla = ?)
                ''', (nro_planilla,))
                for prod in cursor.fetchall():
                    row_pos = self.tabla_productos_reporte.rowCount()
                    self.tabla_productos_reporte.insertRow(row_pos)
                    self.tabla_productos_reporte.setItem(row_pos, 0, QTableWidgetItem(str(prod[0])))
                    self.tabla_productos_reporte.setItem(row_pos, 1, QTableWidgetItem(str(prod[1])))
                    self.tabla_productos_reporte.setItem(row_pos, 2, QTableWidgetItem(str(prod[2])))
                    self.tabla_productos_reporte.setItem(row_pos, 3, QTableWidgetItem(str(prod[3])))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error al cargar reporte", f"Ocurrió un error al cargar el reporte: {str(e)}")
            return
        # Ocultar frames de carga y mostrar el reporte
        if self.frame_6: self.frame_6.setVisible(False)
        if self.frame_10: self.frame_10.setVisible(False)
        if self.frame_reporte: self.frame_reporte.setVisible(True)
        # Actualizar el label para el próximo número
        self.actualizar_label_cod_planilla()

    def volver_de_reporte(self):
        # Ocultar el reporte y mostrar el menú principal
        if self.frame_reporte: self.frame_reporte.setVisible(False)
        if self.frame_6: self.frame_6.setVisible(True)
        if self.frame_10: self.frame_10.setVisible(True)

    def descargar_reporte_imagen(self):
        # Guardar screenshot del frame_reporte como imagen en la carpeta planillas
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtWidgets import QFileDialog
        import os
        if not self.frame_reporte:
            QMessageBox.warning(self, "Error", "No se encontró el frame de reporte para descargar.")
            return
        carpeta = os.path.join(os.getcwd(), 'planillas')
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        nombre = QFileDialog.getSaveFileName(self, "Guardar reporte", carpeta, "Imagen PNG (*.png)")[0]
        if not nombre:
            return
        if not nombre.lower().endswith('.png'):
            nombre += '.png'
        pixmap = QPixmap(self.frame_reporte.size())
        self.frame_reporte.render(pixmap)
        pixmap.save(nombre, 'PNG')

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

    # Versión duplicada eliminada. Usar solo la versión principal de guardar_planilla.

# ------ main -------------
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Main()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())