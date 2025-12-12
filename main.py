from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QPushButton, QTableWidgetItem, QFrame, QInputDialog, QMessageBox, QLabel
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate

import sys
from PyQt5.QtGui import QIcon
import os
import qdarkstyle

from system.localidad.localidad import Localidad
from system.producto.producto import Producto
from system.chofer.chofer import Chofer
from system.vehiculo.vehiculo import Vehiculo
from system.cliente.cliente import Cliente
from system.planilla.planilla import PlanillaWindow

class Main(QMainWindow):
    def init_planilla(self):
        # Inicializar tabla_resumen con nombres de entidades
        self.tabla_resumen = self.findChild(QTableWidget, "tabla_resumen")
        if self.tabla_resumen:
            self.tabla_resumen.setRowCount(4)
            self.tabla_resumen.setColumnCount(2)
            self.tabla_resumen.setHorizontalHeaderLabels(["Entidad", "Detalle"])
            entidades = ["Cliente", "Localidad", "Chofer", "Vehiculo"]
            for i, nombre in enumerate(entidades):
                self.tabla_resumen.setItem(i, 0, QTableWidgetItem(nombre))

        # Conectar botón eliminar selección
        self.btn_eliminar_seleccion = self.findChild(QPushButton, "btn_eliminar_seleccion")
        if self.btn_eliminar_seleccion:
            self.btn_eliminar_seleccion.clicked.connect(self.eliminar_fila_resumen_productos)

        # Conectar botón continuar planilla
        self.btn_continuar_planilla = self.findChild(QPushButton, "btn_continuar_planilla")
        if self.btn_continuar_planilla:
            self.btn_continuar_planilla.clicked.connect(self.guardar_planilla)
        # Conectar botones de agregar entidad para selección en planilla
        self.btn_agregar_cliente_planilla = self.findChild(QPushButton, "btn_agregar_cliente_planilla")
        if self.btn_agregar_cliente_planilla:
            self.btn_agregar_cliente_planilla.clicked.connect(lambda: (self.set_entidad("cliente"), self.mostrar_clientes()))

        self.btn_agregar_localidad_planilla = self.findChild(QPushButton, "btn_agregar_localidad_planilla")
        if self.btn_agregar_localidad_planilla:
            self.btn_agregar_localidad_planilla.clicked.connect(lambda: (self.set_entidad("localidad"), self.mostrar_localidades()))

        self.btn_agregar_chofer_planilla = self.findChild(QPushButton, "btn_agregar_chofer_planilla")
        if self.btn_agregar_chofer_planilla:
            self.btn_agregar_chofer_planilla.clicked.connect(lambda: (self.set_entidad("chofer"), self.mostrar_choferes()))

        self.btn_agregar_vehiculo_planilla = self.findChild(QPushButton, "btn_agregar_vehiculo_planilla")
        if self.btn_agregar_vehiculo_planilla:
            self.btn_agregar_vehiculo_planilla.clicked.connect(lambda: (self.set_entidad("vehiculo"), self.mostrar_vehiculos()))

        self.btn_agregar_producto_planilla = self.findChild(QPushButton, "btn_agregar_producto_planilla")
        if self.btn_agregar_producto_planilla:
            self.btn_agregar_producto_planilla.clicked.connect(lambda: (self.set_entidad("producto"), self.mostrar_productos()))
        # ...resto de la inicialización...

    def eliminar_fila_resumen_productos(self):
        row = self.tabla_resumen_productos.currentRow()
        if row != -1:
            self.tabla_resumen_productos.removeRow(row)
            self.actualizar_total_productos()
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        loadUi('pantallas.ui', self)
        from PyQt5 import QtWidgets, uic, QtCore

        # -------Menu lateral--------
        self.btn_menu = self.findChild(QtWidgets.QToolButton, "btn_menu")
        if self.btn_menu:
            self.btn_menu.clicked.connect(self.toggle_dock)

        # crear dock
        self.menu_dock = QtWidgets.QDockWidget("Menú", self)
        self.menu_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        # cargar el contenido del ui dentro de un widget y setearlo en el dock
        menu_widget = QtWidgets.QWidget()
        uic.loadUi("menu_principal.ui", menu_widget)
        self.menu_dock.setWidget(menu_widget)
        menu_widget.setMinimumWidth(420)
        menu_widget.setMinimumHeight(300)
        self.menu_dock.setMinimumWidth(500)
        self.menu_dock.setMaximumWidth(500)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.menu_dock)
        self.menu_dock.hide()  # empezar oculto

        # --------Estilos y temas ---------
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #bdd4ff;
            }
            QTabBar::tab {
                background: #bdd4ff;
                color: black;
                padding: 6px;
                border: 1px solid #999;
            }
            QTabBar::tab:selected {
                background: #bdd4ff;
                font-weight: bold;
                color: black;
            }
            QTabWidget QWidget {
                background-color: #bdd4ff;
                color: black;
            }
            QTabWidget QPushButton {
                background-color: #e6eeff;
                color: black;
                border: 1px solid #6783b5;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QTabWidget QPushButton:hover {
                background-color: #d0e0ff;
            }
            QTabWidget QPushButton:pressed {
                background-color: #b7cdfa;
            }
        """)

        #----------------Boton configuracion de estilo
        if hasattr(self, 'frameConfiguracion') and self.frameConfiguracion is not None:
            self.frameConfiguracion.setStyleSheet(
                "background-color: #636ae8; color: white; border-radius: 10px; padding: 12px;"
            )
            self.frameConfiguracion.hide()

        # Inicialización de entidades y lógica de pantallas
        self.lastId = 0
        self.selectedId = 0
        self.filaTabla = 0
        self.estado = 'CONSULTAR'
        # ------------- LOCALIDADES
        Localidad.showLocalidades(self)
        Localidad.readLocalidades(self, self.lastId)
        self.btnGuardarLocalidad.clicked.connect(lambda: Localidad.saveLocalidades(self))
        self.btnAgregarLocalidad.clicked.connect(lambda: Localidad.createLocalidades(self))
        self.btnEditarLocalidad.clicked.connect(lambda: Localidad.updateLocalidades(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarLocalidad.clicked.connect(lambda: Localidad.searchLocalidades(self))
        self.tablalocalidad.doubleClicked.connect(lambda: Localidad.doubleClicked_tabla(self))
        self.tablalocalidad.clicked.connect(lambda: Localidad.clicked_tabla(self))
        # ------------- PRODUCTOS
        Producto.showProductos(self)
        self.btnAgregarProducto.clicked.connect(lambda: Producto.createProductos(self))
        self.btnEditarProducto.clicked.connect(lambda: Producto.updateProductos(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarProducto.clicked.connect(lambda: Producto.searchProductos(self))
        self.tablaproductos.doubleClicked.connect(lambda: Producto.doubleClicked_tabla(self))
        self.tablaproductos.clicked.connect(lambda: Producto.clicked_tabla(self))
        # ------------- CHOFERES
        Chofer.showChoferes(self)
        Chofer.readChoferes(self, self.lastId)
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

        # Inicialización de planilla
        self.init_planilla()

        # Ocultar frames de planilla al inicio
        if hasattr(self, 'frame_6') and self.frame_6:
            self.frame_6.setVisible(False)
        if hasattr(self, 'frame_10') and self.frame_10:
            self.frame_10.setVisible(False)

        # Conectar botón para mostrar frames de planilla
        if hasattr(self, 'btn_agregar_planilla_2') and self.btn_agregar_planilla_2:
            self.btn_agregar_planilla_2.clicked.connect(self.mostrar_frames_planilla)
    def mostrar_frames_planilla(self):
        if hasattr(self, 'frame_6') and self.frame_6:
            self.frame_6.setVisible(True)
        if hasattr(self, 'frame_10') and self.frame_10:
            self.frame_10.setVisible(True)

    # --- Métodos de filtrado para tablas de clientes, localidad, chofer, vehiculo y producto ---
    def filtrar_clientes(self, texto):
        if hasattr(self, 'tabla_cliente'):
            for fila in range(self.tabla_cliente.rowCount()):
                item = self.tabla_cliente.item(fila, 1)  # Asume columna 1 es nombre
                self.tabla_cliente.setRowHidden(fila, texto.lower() not in item.text().lower() if item else True)

    def filtrar_localidades(self, texto):
        if hasattr(self, 'tablalocalidad'):
            for fila in range(self.tablalocalidad.rowCount()):
                item = self.tablalocalidad.item(fila, 1)
                self.tablalocalidad.setRowHidden(fila, texto.lower() not in item.text().lower() if item else True)

    def filtrar_choferes(self, texto):
        if hasattr(self, 'tablachoferes'):
            for fila in range(self.tablachoferes.rowCount()):
                item = self.tablachoferes.item(fila, 1)
                self.tablachoferes.setRowHidden(fila, texto.lower() not in item.text().lower() if item else True)

    def filtrar_vehiculos(self, texto):
        if hasattr(self, 'tablavehiculo'):
            for fila in range(self.tablavehiculo.rowCount()):
                item = self.tablavehiculo.item(fila, 1)
                self.tablavehiculo.setRowHidden(fila, texto.lower() not in item.text().lower() if item else True)

    def filtrar_productos(self, texto):
        if hasattr(self, 'tablaproductos'):
            for fila in range(self.tablaproductos.rowCount()):
                item = self.tablaproductos.item(fila, 1)
                self.tablaproductos.setRowHidden(fila, texto.lower() not in item.text().lower() if item else True)

        # Inicialización de planillas y lógica de panel
        self.init_planilla()
        # Conexión de botones para seleccionar entidad en planilla (solo si existen)
        # (Evitar duplicados, solo conectar en init_planilla)
        # Conexión del botón para mostrar frames de planilla
        if self.btn_agregar_planilla_2:
            self.btn_agregar_planilla_2.clicked.connect(self.mostrar_frames_planilla)
        self.icono_sol = os.path.join('imagenes', 'modoclaro.png')
        self.icono_luna = os.path.join('imagenes', 'modooscuro.png')
        try:
            if hasattr(self, 'btnModo'):
                if os.path.exists(self.icono_luna) and self.is_dark:
                    self.btnModo.setIcon(QIcon(self.icono_luna))
                elif os.path.exists(self.icono_sol) and not self.is_dark:
                    self.btnModo.setIcon(QIcon(self.icono_sol))
                self.btnModo.clicked.connect(self.toggle_theme)
        except Exception:
            pass
        try:
            if qdarkstyle is not None:
                QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            else:
                dark = """
                QWidget{background-color:#2b2b2b;color:#e6e6e6}
                QPushButton{background-color:#3c3f41;color:#e6e6e6}
                """
                QApplication.instance().setStyleSheet(dark)
        except Exception:
            pass

    def toggle_theme(self):
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon
        import os
        try:
            if self.is_dark:
                QApplication.instance().setStyleSheet("")
                try:
                    if os.path.exists(self.icono_sol):
                        self.btnModo.setIcon(QIcon(self.icono_sol))
                except Exception:
                    pass
                self.is_dark = False
            else:
                import qdarkstyle
                if qdarkstyle is not None:
                    QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
                else:
                    dark = """
                    QWidget{background-color:#2b2b2b;color:#e6e6e6}
                    QPushButton{background-color:#3c3f41;color:#e6e6e6}
                    """
                    QApplication.instance().setStyleSheet(dark)
                try:
                    if os.path.exists(self.icono_luna):
                        self.btnModo.setIcon(QIcon(self.icono_luna))
                except Exception:
                    pass
                self.is_dark = True
        except Exception:
            pass

    def toggle_dock(self):
        visible = self.menu_dock.isVisible()
        self.menu_dock.setVisible(not visible)

    def toggleConfiguracion(self):
        if not hasattr(self, 'frameConfiguracion') or self.frameConfiguracion is None:
            return
        if self.frameConfiguracion.isVisible():
            self.frameConfiguracion.hide()
        else:
            self.frameConfiguracion.show()

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
        # Conectar lineEdits de búsqueda a los métodos de filtrado
        if hasattr(self, 'lineEdit_buscar_cliente'):
            self.lineEdit_buscar_cliente.textChanged.connect(self.filtrar_clientes)
        if hasattr(self, 'lineEdit_buscar_localidad'):
            self.lineEdit_buscar_localidad.textChanged.connect(self.filtrar_localidades)
        if hasattr(self, 'lineEdit_buscar_chofer'):
            self.lineEdit_buscar_chofer.textChanged.connect(self.filtrar_choferes)
        if hasattr(self, 'lineEdit_buscar_vehiculo'):
            self.lineEdit_buscar_vehiculo.textChanged.connect(self.filtrar_vehiculos)
        if hasattr(self, 'lineEdit_buscar_producto'):
            self.lineEdit_buscar_producto.textChanged.connect(self.filtrar_productos)

        self.ultima_entidad = None
        self.cliente_seleccionado = None
        self.localidad_seleccionada = None
        self.chofer_seleccionado = None
        self.vehiculo_seleccionado = None
        self.id_cliente_seleccionado = None
        self.id_localidad_seleccionada = None
        self.id_chofer_seleccionado = None
        self.id_vehiculo_seleccionado = None
        # ...existing code...
        # Eliminar conexión innecesaria:
        # self.btn_buscar_3.clicked.connect(self.buscar_en_tabla_seleccionar)
        if hasattr(self, 'btn_agregar_a_planilla'):
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
        print(f"set_entidad llamado con: {entidad}")
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
            QMessageBox.warning(self, "Selección requerida", "Debe seleccionar una fila para agregar.")
            return

        # ENTIDADES: cliente, localidad, chofer, vehiculo
        if self.ultima_entidad in ['cliente', 'localidad', 'chofer', 'vehiculo']:
            id_item = self.tabla_seleccionar_datos.item(row, 0)
            nombre_item = self.tabla_seleccionar_datos.item(row, 1)
            nombre = nombre_item.text() if nombre_item else ""
            if self.ultima_entidad == 'cliente':
                self.id_cliente_seleccionado = id_item.text() if id_item else None
                if self.tabla_resumen:
                    self.tabla_resumen.setItem(0, 1, QTableWidgetItem(nombre))
                QMessageBox.information(self, "Cliente agregado", f"Cliente: {nombre}")
            elif self.ultima_entidad == 'localidad':
                self.id_localidad_seleccionada = id_item.text() if id_item else None
                if self.tabla_resumen:
                    self.tabla_resumen.setItem(1, 1, QTableWidgetItem(nombre))
                QMessageBox.information(self, "Localidad agregada", f"Localidad: {nombre}")
            elif self.ultima_entidad == 'chofer':
                self.id_chofer_seleccionado = id_item.text() if id_item else None
                if self.tabla_resumen:
                    self.tabla_resumen.setItem(2, 1, QTableWidgetItem(nombre))
                QMessageBox.information(self, "Chofer agregado", f"Chofer: {nombre}")
            elif self.ultima_entidad == 'vehiculo':
                self.id_vehiculo_seleccionado = id_item.text() if id_item else None
                if self.tabla_resumen:
                    self.tabla_resumen.setItem(3, 1, QTableWidgetItem(nombre))
                QMessageBox.information(self, "Vehículo agregado", f"Vehículo: {nombre}")
            return

        # PRODUCTO
        if self.ultima_entidad == 'producto':
            # Buscar índices de columnas relevantes
            headers = [self.tabla_seleccionar_datos.horizontalHeaderItem(j).text() for j in range(self.tabla_seleccionar_datos.columnCount())]
            try:
                idx_id = headers.index('ID')
                idx_detalle = headers.index('Descripción')
                idx_precio = headers.index('Precio')
            except ValueError:
                QMessageBox.warning(self, "Error", "No se pudo obtener los datos del producto.")
                return
            id_producto = self.tabla_seleccionar_datos.item(row, idx_id).text() if self.tabla_seleccionar_datos.item(row, idx_id) else ""
            detalle = self.tabla_seleccionar_datos.item(row, idx_detalle).text() if self.tabla_seleccionar_datos.item(row, idx_detalle) else ""
            try:
                precio = float(self.tabla_seleccionar_datos.item(row, idx_precio).text())
            except Exception:
                QMessageBox.warning(self, "Error", "El precio no es válido.")
                return
            cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"Ingrese la cantidad para '{detalle}':", 1, 1)
            if not ok:
                return
            subtotal = precio * cantidad
            # Buscar si el producto ya existe en la tabla resumen_productos
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
                QMessageBox.information(self, "Producto actualizado", f"Se actualizó la cantidad de '{detalle}' en la planilla.")
            else:
                row_pos = self.tabla_resumen_productos.rowCount()
                self.tabla_resumen_productos.insertRow(row_pos)
                self.tabla_resumen_productos.setItem(row_pos, 0, QTableWidgetItem(str(id_producto)))
                self.tabla_resumen_productos.setItem(row_pos, 1, QTableWidgetItem(detalle))
                self.tabla_resumen_productos.setItem(row_pos, 2, QTableWidgetItem(f"{precio:.2f}"))
                self.tabla_resumen_productos.setItem(row_pos, 3, QTableWidgetItem(str(cantidad)))
                self.tabla_resumen_productos.setItem(row_pos, 4, QTableWidgetItem(f"{subtotal:.2f}"))
                QMessageBox.information(self, "Producto agregado", f"Se agregó '{detalle}' a la planilla.")
            self.actualizar_total_productos()

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