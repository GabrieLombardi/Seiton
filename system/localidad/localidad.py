import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from tools.DBCrud import CRUD

class Localidad():
    """Clase especifidica de las Localidades """
    nombre=""
    cod_postal=""

    def __init__ (self,nombreloc,cod_postal,):
        self.nombreloc=nombreloc
        self.cod_postal=cod_postal
        self.index=0
        
    def showLocalidades(self): # Muestro Categorias
        ''' muestro Localidades '''
        Localidades = Localidad.readLocalidades(self,self.lastId) # leo los Categorias
        # cargo la tabla del qtDesigner con los Categorias consultados
        for localidads1 in Localidades:
            id_localidad = localidads1[0] # ID
            nombreloc = localidads1[1] # CATEGORIA
            cod_postal = localidads1[2] # CATEGORIA
            print(localidads1)

            self.tablalocalidad.setRowCount(self.index + 1) #Agrego una fila
            self.tablalocalidad.setItem(self.index, 0, QTableWidgetItem(str(id_localidad))) #Cargo el ID en la fila creada
            self.tablalocalidad.setItem(self.index, 1, QTableWidgetItem(nombreloc)) #Cargo la CATEGORIA en la fila creada
            self.tablalocalidad.setItem(self.index, 2, QTableWidgetItem(str(cod_postal))) 
            self.index += 1 #Incremento el indexador
            #En variables almaceno y llamo a las funciones que se necesitan desde el inicio
        # mostrarCategorias = Localidad.llenarcomboboxCategorias(self, nombreloc,cod_postal)
        # mostrarFiltroCategorias=Localidad.llenarFiltro(self, nombreloc,cod_postal)
        # verCategoriasventa= Localidad.llenolocalidad_venta(self, nombreloc,cod_postal)
    
    def readLocalidades(self,Id_Localidad):
        '''leo Categorias'''
        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if Id_Localidad > 0:
            miConsulta = "SELECT * FROM localidad WHERE ID = " + str(Id_Localidad) +";"
            self.index=self.tablalocalidad.rowCount() #cuento cuantos registro tiene la tablaCategorias 
            # print('index:',index)
        else:
            # Establecer ancho de las columnas cuando paso por primera vez
            for indice, ancho in enumerate((10, 300,300), start=0):
                self.tablalocalidad.setColumnWidth(indice, ancho)

            miConsulta = "SELECT * FROM localidad;"
            self.index=0
        
        localidads=miCrud.Read(miConsulta) #Ejecuto Read de miCrud (ver instanciamiento más arriba)
        return localidads
        
        
    def saveLocalidades(self):
        """Guarda y actualiza lo modificado en la BD"""
        self.localidad = self.lineEdit_localidad.text().upper()
        self.localidad = self.lineEdit_codpost.text()


        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if self.estado=='AGREGAR':
            misDatos = (self.localidad,self.cod_postal)
            miConsulta = "INSERT INTO localidad (nombreloc) VALUES (?);(cod_postal) VALUES (?);"
            miCrud.Create(miConsulta, (misDatos,)) #Ejecuto Create de miCrud (ver instanciamiento más arriba)
        elif self.estado=='EDITAR':
            miConsulta = "UPDATE localidad SET  nombreloc = ?; cod_postal =?  WHERE Id_localidad = ?;"
            misDatos = (self.localidad, self.selectedId)
            miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        elif self.estado== 'ELIMINAR':
            miConsulta="DELETE from localidad where Id_localidad=?;"
            misDatos=(self.selectedId)
            miCrud.Delete(miConsulta,(misDatos,))
        Localidad.readLocalidades(self, 0)
        self.lineEdit_localidad.clear()
        self.lineEdit_codpost.clear()
        self.estado = 'CONSULTAR'
        
        Localidad.showLocalidades(self)


    # def llenarcomboboxCategorias(self, Categoria):
    #     """Carga el combo usado en la seccion de productos"""
    #     Categoria= Categorias.readCategorias(self, self.lastId)
    #     self.comboboxCategorias.clear()
    #     for localidads1 in Categoria:
    #         id_localidad = localidads1[0] # ID
    #         localidad = localidads1[1] # CATEGORIA
    #         self.comboboxCategorias.addItem(localidad, id_localidad)
    #         self.comboboxCategorias.setDisabled(True)

    # def llenarFiltro(self, Categoria):
    #     """Llena el combobox de las localidads a filtrar."""
    #     localidads= Categorias.readCategorias(self, self.lastId)
    #     self.comboboxFiltro.clear()
    #     for localidad in localidads:
    #         self.comboboxFiltro.addItem(localidad[1], localidad[0])


    # def llenolocalidad_venta(self,Categoria):
    #     """Permite filtrar por localidads en la seccion de ventas"""
    #     Categoria= Categorias.readCategorias(self, self.lastId)
    #     self.comboBox_localidad.clear()
    #     for localidads1 in Categoria:
    #         id_localidad = localidads1[0] # ID
    #         localidad = localidads1[1] # CATEGORIA
    #         self.comboBox_localidad.addItem(localidad, id_localidad)



    def searchLocalidades(self):
        """Realiza la busqueda de las localidads mediante lo que se ingresa en el lineedit"""
        self.conexion_BD = sqlite3.connect("pedidos.sqlite3")
        self.cursor = self.conexion_BD.cursor()
        buscar = self.lineEdit.text()
        self.cursor.execute("SELECT * FROM localidad WHERE localidad LIKE ?", ('%' + buscar + '%',))
        localidads = self.cursor.fetchall()
        self.tablalocalidad.setRowCount(0)
        for localidad in localidads:
            row_position = self.tablalocalidad.rowCount()
            self.tablalocalidad.insertRow(row_position)
            self.tablalocalidad.setItem(row_position, 0, QTableWidgetItem(str(localidad[0])))
            self.tablalocalidad.setItem(row_position, 1, QTableWidgetItem(localidad[1]))
    

    def createLocalidades(self):
        self.estado='AGREGAR'
        self.lineEdit_localidad.clear()
        
        # mandar el foco a lineedit_nombre
        self.lineEdit_localidad.setFocus()

    def updateLocalidades(self): # modificar Categorias
        self.estado='EDITAR'
        self.selectedId = self.tablalocalidad.item(self.tablalocalidad.currentRow(), 0).text()
        self.lineEdit_localidad.setText(self.tablalocalidad.item(self.tablalocalidad.currentRow(), 1).text())
        self.lineEdit_codpost.setText(self.tablalocalidad.item(self.tablalocalidad.currentRow(), 2).text())

        # mandar el foco a lineedit_nombre
        self.lineEdit_localidad.setFocus()       

    def deleteLocalidades(self):
        self.estado='ELIMINAR'
        import sqlite3

        # Conectar a la base de datos
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        self.selectedId = self.tablalocalidad.item(self.tablalocalidad.currentRow(), 0).text()
        # Eliminar un registro
        cursor.execute('DELETE FROM localidad WHERE id_localidad = ?', (self.selectedId,))
        # Confirmar los cambios
        conn.commit()
        # Cerrar la conexión
        conn.close()
        miCrud=CRUD()
        miConsulta = "UPDATE Categorias SET localidad= ? WHERE id_localidad = ?;"

        # misDatos = (self.localidad, self.selectedId)
        misDatos = (self.localidad, self.selectedId)

        miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        
        Localidad.readLocaliades(self, 0)
        
        Localidad.showLocalidades(self)
    
    def doubleClicked_tabla(self):
        pass

    def clicked_tabla(self):
        pass