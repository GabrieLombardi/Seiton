import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from tools.DBCrud import CRUD
from PyQt5.QtCore import QDate

class Chofer():
    """Clase especifidica de las Choferes """
    nombre=""
    cuit=""
    dni=""
    fn=""
    direccion=""
    tel=""


    def __init__ (self,nombre,cuit,dni,fn,tel,direccion):
        self.nombre=nombre
        self.cuit=cuit
        self.dni=dni
        self.fn=fn
        self.tel=tel
        self.direccion=direccion
        self.index=0
        
    def showChoferes(self): # Muestro Categorias
        ''' muestro Choferes '''
        Choferes= Chofer.readChoferes(self,self.lastId) # leo los Categorias
        # cargo la tabla del qtDesigner con los Categorias consultados
        for chofers1 in Choferes:
            id_chofer = chofers1[0] # ID
            nombre=chofers1 [1] #nombre
            cuit=chofers1[2] # dni 
            dni=chofers1[3] # dni
            fn=chofers1[4] # fn
            tel=chofers1[5] # tel
            direccion=chofers1[6] # direccion
    
            print(chofers1)

            self.tablachoferes.setRowCount(self.index + 1) #Agrego una fila
            self.tablachoferes.setItem(self.index, 0, QTableWidgetItem(str(id_chofer))) #Cargo el ID en la fila creada
            self.tablachoferes.setItem(self.index, 1, QTableWidgetItem(nombre)) #Cargo la CATEGORIA en la fila creada
            self.tablachoferes.setItem(self.index, 2, QTableWidgetItem(str(cuit))) 
            self.tablachoferes.setItem(self.index, 3, QTableWidgetItem(str(dni)))
            self.tablachoferes.setItem(self.index, 4, QTableWidgetItem(str(fn)))
            self.tablachoferes.setItem(self.index, 5, QTableWidgetItem(str(tel)))
            self.tablachoferes.setItem(self.index, 6, QTableWidgetItem(direccion))

            self.index += 1 #Incremento el indexador

            #En variables almaceno y llamo a las funciones que se necesitan desde el inicio

    
    def readChoferes(self,Id_Chofer):
        '''leo Choferes'''
        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if Id_Chofer > 0:
            miConsulta = "SELECT * FROM chofer WHERE ID = " + str(Id_Chofer) +";"
            self.index=self.tablachoferes.rowCount() #cuento cuantos registro tiene la tablachoferes 
            # print('index:',index)
        else:
            # Establecer ancho de las columnas cuando paso por primera vez
            for indice, ancho in enumerate((10, 200,100,100,100,120,150), start=0):
                self.tablachoferes.setColumnWidth(indice, ancho)

            miConsulta = "SELECT * FROM chofer;"
            self.index=0
        
        choferes=miCrud.Read(miConsulta) #Ejecuto Read de miCrud (ver instanciamiento más arriba)
        return choferes
        
        
    def saveChoferes(self):
        """Guarda y actualiza lo modificado en la BD"""
        self.nombre = self.lineEdit_nombre_chofer.text().upper()
        self.cuit= self.lineEdit_cuit.text()
        self.dni = self.lineEdit_dni.text()
        self.fn = self.editdate.date().toString("yyyy-MM-dd")
        self.direccion = self.lineEdit_direccion.text().upper()
        self.tel = self.lineEdit_tel.text()
        


        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if self.estado=='AGREGAR':
            misDatos = (self.nombre,self.cuit,self.dni,self.fn,self.tel,self.direccion)
            miConsulta = "INSERT INTO Chofer (nombre,cuit,dni,fn,tel,direccion) VALUES (?,?,?,?,?,?);"
            miCrud.Create(miConsulta,misDatos) #Ejecuto Create de miCrud (ver instanciamiento más arriba)
        elif self.estado=='EDITAR':
            miConsulta = "UPDATE chofer SET  nombre = ?, cuit =?, dni =?, fn =?, tel =?, direccion =?  WHERE Id_chofer = ?;"
            misDatos = (self.nombre,self.cuit,self.dni,self.fn,self.tel,self.direccion, self.selectedId)
            miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        elif self.estado== 'ELIMINAR':
            miConsulta="DELETE from chofer where Id_chofer=?;"
            misDatos=(self.selectedId)
            miCrud.Delete(miConsulta,(misDatos,))
        Chofer.readChoferes(self, 0)
        self.lineEdit_nombre_chofer.clear()
        self.lineEdit_cuit.clear()
        self.lineEdit_dni.clear()
        self.editdate.setDate(QDate(2022, 12, 18))
        self.lineEdit_tel.clear()
        self.lineEdit_direccion.clear()

        self.estado = 'CONSULTAR'
        
        Chofer.showChoferes(self)


    # def llenarcomboboxCategorias(self, Categoria):
    #     """Carga el combo usado en la seccion de Choferes"""
    #     Categoria= Categorias.readCategorias(self, self.lastId)
    #     self.comboboxCategorias.clear()
    #     for productos1 in Categoria:
    #         id_localidad = productos1[0] # ID
    #         localidad = productos1[1] # CATEGORIA
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
    #     for productos1 in Categoria:
    #         id_localidad = productos1[0] # ID
    #         localidad = productos1[1] # CATEGORIA
    #         self.comboBox_localidad.addItem(localidad, id_localidad)



    def searchChoferes(self):
        """Realiza la busqueda de las localidads mediante lo que se ingresa en el lineedit"""
        self.conexion_BD = sqlite3.connect("pedidos.sqlite3")
        self.cursor = self.conexion_BD.cursor()
        buscar = self.lineEdit_buscarchofer.text()
        self.cursor.execute("SELECT * FROM chofer WHERE nombre LIKE ?", ('%' + buscar + '%',))
        Choferes= self.cursor.fetchall()
        self.tablachoferes.setRowCount(0)
        for chofers1 in Choferes:
            row_position = self.tablachoferes.rowCount()
            self.tablachoferes.insertRow(row_position)
            self.tablachoferes.setItem(row_position, 0, QTableWidgetItem(str(chofers1[0])))
            self.tablachoferes.setItem(row_position, 1, QTableWidgetItem(chofers1[1]))
            self.tablachoferes.setItem(row_position, 2, QTableWidgetItem(str(chofers1[2])))
            self.tablachoferes.setItem(row_position, 3, QTableWidgetItem(str(chofers1[3])))
            self.tablachoferes.setItem(row_position, 4, QTableWidgetItem(str(chofers1[4])))
            self.tablachoferes.setItem(row_position, 5, QTableWidgetItem(str(chofers1[5])))
            self.tablachoferes.setItem(row_position, 6, QTableWidgetItem(str(chofers1[6])))                  
    

    def createChoferes(self):
        self.estado='AGREGAR'
        self.lineEdit_nombre_chofer.clear()
        self.lineEdit_nombre_chofer.setEnabled(True) # activa el lineedit nombre
        self.lineEdit_nombre_chofer.setFocus() # mandar el foco a lineedit nombre
        self.lineEdit_cuit.clear()
        self.lineEdit_cuit.setEnabled(True) #activa el lineEdit cuit
        self.lineEdit_dni.clear()
        self.lineEdit_dni.setEnabled(True)  # activa el lineedit dni
        self.editdate.setDate(QDate.currentDate())
        self.editdate.setEnabled(True)  # activa el dateedit fn
        self.lineEdit_direccion.clear()
        self.lineEdit_direccion.setEnabled(True)  # activa el lineedit direccion
        self.lineEdit_tel.clear()
        self.lineEdit_tel.setEnabled(True)  # activa el lineedit tel
        

    def updateChoferes(self): # modificar Choferes
        self.estado='EDITAR'
        self.selectedId = self.tablachoferes.item(self.tablachoferes.currentRow(), 0).text()
        self.lineEdit_nombre_chofer.setText(self.tablachoferes.item(self.tablachoferes.currentRow(), 1).text())
        self.lineEdit_cuit.setText(self.tablachoferes.item(self.tablachoferes.currentRow(), 2).text())
        self.lineEdit_dni.setText(self.tablachoferes.item(self.tablachoferes.currentRow(), 3).text())
        fecha_nac = self.tablachoferes.item(self.tablachoferes.currentRow(), 4).text()
        self.editdate.setDate(QDate.fromString(fecha_nac, "yyyy-MM-dd"))
        self.lineEdit_tel.setText(self.tablachoferes.item(self.tablachoferes.currentRow(), 5).text())
        self.lineEdit_direccion.setText(self.tablachoferes.item(self.tablachoferes.currentRow(), 6).text())
    
        # mandar el foco a lineedit_nombre
        self.lineEdit_nombre_chofer.setEnabled(True) # activa el lineedit descripcion
        self.lineEdit_nombre_chofer.setFocus() 
        self.lineEdit_cuit.setEnabled(True) #activa el lineEdit cuit
        self.lineEdit_dni.setEnabled(True)  # activa el lineedit dni
        self.editdate.setEnabled(True)  # activa el dateedit fn
        self.lineEdit_tel.setEnabled(True)  # activa el lineedit tel
        self.lineEdit_direccion.setEnabled(True)  # activa el lineedit direccion
    

    def deleteChoferes(self):
        self.estado='ELIMINAR'
        import sqlite3

        # Conectar a la base de datos
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        self.selectedId = self.tablachoferes.item(self.tablachoferes.currentRow(), 0).text()
        # Eliminar un registro
        cursor.execute('DELETE FROM Chofer WHERE id_chofer = ?', (self.selectedId,))
        # Confirmar los cambios
        conn.commit()
        # Cerrar la conexión
        conn.close()
        miCrud=CRUD()
        miConsulta = "UPDATE chofer SET nombre= ? WHERE id_chofer = ?;"

        # misDatos = (self.nombre, self.selectedId)
        misDatos = (self.nombre, self.selectedId)

        miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        
        Chofer.readChoferes(self, 0)
        
        Chofer.showChoferes(self)
    
    def doubleClicked_tabla(self):
        pass

    def clicked_tabla(self):
        pass