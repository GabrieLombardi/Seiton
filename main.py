from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi


import sys
from system.localidad.localidad import Localidad
from system.producto.producto import Producto
from system.chofer.chofer import Chofer

class Main(QMainWindow):
    def __init__(self, parent=None):

        super(Main, self).__init__(parent)
        loadUi('pantallas.ui', self)
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


def showLocalidades():
        Localidad.showLocalidades()
def showProductos():
        Producto.showProductos()
def showChoferes():
        Chofer.showChoferes()

# ------ main -------------
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Main()
    mi_app.show()
    sys.exit(mi_aplicacion.exec_())