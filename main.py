from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi


import sys
from system.localidad.localidad import Localidad 

class Main(QMainWindow):
    def __init__(self, parent=None):

        super(Main, self).__init__(parent)
        loadUi('main.ui', self)
        # defino las variables que voy a utilizar
        self.lastId=0
        self.selectedId=0
        self.filaTabla=0
        self.estado='CONSULTAR'   

        #------------- CATEGORIAS
        Localidad.showLocalidades(self) #primero muestro contenidos en la pantalla
        Localidad.readLocaliades(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarLocalidad.clicked.connect(lambda: Localidad.saveLocalidades(self))

        self.btnAgregarLocalidad.clicked.connect(lambda: Localidad.createLocalidades(self))
        self.btnEditarLocalidad.clicked.connect(lambda: Localidad.updateLocalidades(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarLocalidad.clicked.connect(lambda: Localidad.searchLocalidades(self))

        self.tablalocalidad.doubleClicked.connect(lambda: Localidad.doubleClicked_tabla(self))    
        self.tablalocalidad.clicked.connect(lambda: Localidad.clicked_tabla(self))