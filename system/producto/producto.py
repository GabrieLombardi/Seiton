import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from tools.DBCrud import CRUD
from PyQt5.QtWidgets import QMessageBox

class Producto():
    """Clase especifidica de las Productos """
    descripcion=""
    cod_producto=""
    precio_unid=""

    def __init__ (self,descripcion,cod_producto,precio_unid,):
        self.descripcion=descripcion 
        self.cod_producto=cod_producto
        self.precio_unid=precio_unid
        self.index=0
        
    def showProductos(self): # Muestro Categorias
        ''' muestro Productos '''
        Productos = Producto.readProductos(self,self.lastId) # leo los Categorias
        # cargo la tabla del qtDesigner con los Categorias consultados
        for productos1 in Productos:
            id_producto = productos1[0] # ID
            descripcion= productos1[1] # descripcion
            cod_producto = productos1[2] # cod_producto
            precio_unid= productos1[3] # precio_unid
            
            print(productos1)

            self.tablaproductos.setRowCount(self.index + 1) #Agrego una fila
            self.tablaproductos.setItem(self.index, 0, QTableWidgetItem(str(id_producto))) #Cargo el ID en la fila creada
            self.tablaproductos.setItem(self.index, 1, QTableWidgetItem(descripcion)) #Cargo la CATEGORIA en la fila creada
            self.tablaproductos.setItem(self.index, 2, QTableWidgetItem(str(cod_producto))) 
            self.tablaproductos.setItem(self.index, 3, QTableWidgetItem(str(precio_unid)))
            self.index += 1 #Incremento el indexador
            #En variables almaceno y llamo a las funciones que se necesitan desde el inicio
        # mostrarCategorias = Localidad.llenarcomboboxCategorias(self, nombreloc,cod_postal)
        # mostrarFiltroCategorias=Localidad.llenarFiltro(self, nombreloc,cod_postal)
        # verCategoriasventa= Localidad.llenolocalidad_venta(self, nombreloc,cod_postal)
    
    def readProductos(self,Id_Producto):
        '''leo Productos'''
        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if Id_Producto > 0:
            miConsulta = "SELECT * FROM Producto WHERE ID = " + str(Id_Producto) +";"
            self.index=self.tablaproductos.rowCount() #cuento cuantos registro tiene la tablaCategorias 
            # print('index:',index)
        else:
            # Establecer ancho de las columnas cuando paso por primera vez
            for indice, ancho in enumerate((10, 200,120,120), start=0):
                self.tablaproductos.setColumnWidth(indice, ancho)

            miConsulta = "SELECT * FROM Producto;"
            self.index=0
        
        productos=miCrud.Read(miConsulta) #Ejecuto Read de miCrud (ver instanciamiento más arriba)
        return productos
        
        
    def saveProductos(self):
        """Guarda y actualiza lo modificado en la BD"""
        self.descripcion = self.lineEdit_descripcion.text().upper()
        self.cod_producto= self.lineEdit_codproducto.text()
        self.precio_unid = self.lineEdit_preciounid.text()
        self.precio_unid = float(self.precio_unid) if self.precio_unid else 0.0
        #Desactivar los lineedits despues de guardar
        self.lineEdit_descripcion.setEnabled(False) # desactiva el lineedit descripcion
        self.lineEdit_codproducto.setEnabled(False) #desactiva el lineEdit cod_producto 
        self.lineEdit_preciounid.setEnabled(False)  # desactiva el lineedit precio_unid


        miCrud=CRUD() #instancio la clase CRUD del módulo DBCrud.py de herramientas
        if self.estado=='AGREGAR':
            misDatos = (self.descripcion,self.cod_producto,self.precio_unid)
            miConsulta = "INSERT INTO Producto (descripcion, cod_producto,precio_unid) VALUES (?,?,?);"
            miCrud.Create(miConsulta,misDatos) #Ejecuto Create de miCrud (ver instanciamiento más arriba)
        elif self.estado=='EDITAR':
            miConsulta = "UPDATE Producto SET  descripcion = ?, cod_producto =?, precio_unid =?  WHERE Id_producto = ?;"
            misDatos = (self.descripcion,self.cod_producto,self.precio_unid, self.selectedId)
            miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        elif self.estado== 'ELIMINAR':
            miConsulta="DELETE from Producto where Id_producto=?;"
            misDatos=(self.selectedId)
            miCrud.Delete(miConsulta,(misDatos,))
        Producto.readProductos(self, 0)
        self.lineEdit_descripcion.clear()
        self.lineEdit_codproducto.clear()
        self.lineEdit_preciounid.clear()
        self.estado = 'CONSULTAR'
        
        Producto.showProductos(self)


    # def llenarcomboboxCategorias(self, Categoria):
    #     """Carga el combo usado en la seccion de productos"""
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



    def searchProductos(self):
        """Realiza la busqueda de las localidads mediante lo que se ingresa en el lineedit"""
        self.conexion_BD = sqlite3.connect("pedidos.sqlite3")
        self.cursor = self.conexion_BD.cursor()
        buscar = self.lineEdit_buscar_prod.text()
        self.cursor.execute("SELECT * FROM Producto WHERE descripcion LIKE ?", ('%' + buscar + '%',))
        Productos= self.cursor.fetchall()
        self.tablaproductos.setRowCount(0)
        for productos1 in Productos:
            row_position = self.tablaproductos.rowCount()
            self.tablaproductos.insertRow(row_position)
            self.tablaproductos.setItem(row_position, 0, QTableWidgetItem(str(productos1[0])))
            self.tablaproductos.setItem(row_position, 1, QTableWidgetItem(productos1[1]))
            self.tablaproductos.setItem(row_position, 2, QTableWidgetItem(str(productos1[2])))
            self.tablaproductos.setItem(row_position, 3, QTableWidgetItem(str(productos1[3])))
    

    def createProductos(self):
        self.estado='AGREGAR'
        self.lineEdit_descripcion.clear()
        self.lineEdit_descripcion.setEnabled(True) # activa el lineedit descripcion
        self.lineEdit_descripcion.setFocus() # mandar el foco a lineedit descripcion
        
        
        self.lineEdit_codproducto.clear()
        self.lineEdit_codproducto.setEnabled(True) #activa el lineEdit cod_producto
        self.lineEdit_preciounid.clear()
        self.lineEdit_preciounid.setEnabled(True)  # activa el lineedit precio_unid

    def updateProductos(self): # modificar Categorias
        self.estado='EDITAR'
        self.selectedId = self.tablaproductos.item(self.tablaproductos.currentRow(), 0).text()
        self.lineEdit_descripcion.setText(self.tablaproductos.item(self.tablaproductos.currentRow(), 1).text())
        self.lineEdit_codproducto.setText(self.tablaproductos.item(self.tablaproductos.currentRow(), 2).text())
        self.lineEdit_preciounid.setText(self.tablaproductos.item(self.tablaproductos.currentRow(), 3).text())

        # mandar el foco a lineedit_nombre
        self.lineEdit_descripcion.setEnabled(True) # activa el lineedit descripcion
        self.lineEdit_descripcion.setFocus() 
        self.lineEdit_codproducto.setEnabled(True) #activa el lineEdit cod_producto
        self.lineEdit_preciounid.setEnabled(True)  # activa el lineedit precio_un      

    def deleteProductos(self):
        self.estado='ELIMINAR'
        import sqlite3

        # Conectar a la base de datos
        conn = sqlite3.connect('pedidos.sqlite3')
        cursor = conn.cursor()
        self.selectedId = self.tablaproductos.item(self.tablaproductos.currentRow(), 0).text()
        # Eliminar un registro
        cursor.execute('DELETE FROM Producto WHERE id_producto = ?', (self.selectedId,))
        # Confirmar los cambios
        conn.commit()
        # Cerrar la conexión
        conn.close()
        miCrud=CRUD()
        miConsulta = "UPDATE Producto SET descripcion= ? WHERE id_producto = ?;"

        # misDatos = (self.descripcion, self.selectedId)
        misDatos = (self.descripcion, self.selectedId)

        miCrud.Update(miConsulta, (misDatos,)) #Ejecuto Update de miCrud (ver instanciamiento más arriba)
        
        Producto.readProductos(self, 0)
        
        Producto.showProductos(self)
    
    def doubleClicked_tabla(self):
        pass

    def clicked_tabla(self):
        pass