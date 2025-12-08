import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
from tools.DBCrud import CRUD


class Vehiculo():
    """Clase específica de Vehículos"""
    matricula = ""
    descripcion = ""
    disponibilidad = ""

    def _init_(self, matricula, descripcion, disponibilidad):
        self.matricula = matricula
        self.descripcion = descripcion
        self.disponibilidad = disponibilidad

    def searchVehiculos(self, main_window):
        """Realiza la búsqueda de vehículos mediante lo ingresado en el lineEdit."""
        try:
            main_window.tablavehiculo.setColumnCount(4)
            main_window.tablavehiculo.setHorizontalHeaderLabels(["ID", "Matrícula", "Descripción", "Disponibilidad"])
            conexion_BD = sqlite3.connect("pedidos.sqlite3")
            cursor = conexion_BD.cursor()
            buscar = main_window.lineEdit_buscar_2.text()
            cursor.execute("SELECT * FROM vehiculo WHERE matricula LIKE ?", ('%' + buscar + '%',))
            Vehiculos = cursor.fetchall()
            main_window.tablavehiculo.setRowCount(0)
            for vehiculo1 in Vehiculos:
                row_position = main_window.tablavehiculo.rowCount()
                main_window.tablavehiculo.insertRow(row_position)
                main_window.tablavehiculo.setItem(row_position, 0, QTableWidgetItem(str(vehiculo1[0])))
                main_window.tablavehiculo.setItem(row_position, 1, QTableWidgetItem(vehiculo1[1]))
                main_window.tablavehiculo.setItem(row_position, 2, QTableWidgetItem(vehiculo1[2]))
                main_window.tablavehiculo.setItem(row_position, 3, QTableWidgetItem(str(vehiculo1[3])))
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al buscar vehículos: {e}")

    def readVehiculos(self, main_window, Id_Vehiculo):
        """Lee vehículos desde la BD; si Id_Vehiculo>0 filtra por id."""
        miCrud = CRUD()
        if Id_Vehiculo > 0:
            miConsulta = "SELECT * FROM vehiculo WHERE ID = " + str(Id_Vehiculo) + ";"
            index = main_window.tablavehiculo.rowCount()
        else:
            # Establecer ancho de las columnas cuando paso por primera vez
            for indice, ancho in enumerate((10, 200, 100, 100), start=0):
                main_window.tablavehiculo.setColumnWidth(indice, ancho)

            miConsulta = "SELECT * FROM vehiculo;"
            index = 0

        vehiculos = miCrud.Read(miConsulta)
        return vehiculos

    def saveVehiculos(self, main_window):
        """Guarda o actualiza un vehículo en la BD."""
        try:
            matricula = main_window.lineEdit_matricula.text().upper()
            descripcion = main_window.lineEdit_descripcionVehiculo.text().upper()
            disponibilidad = "Sí" if main_window.checkBox_vehiculo.isChecked() else "No"
            miCrud = CRUD()
            if main_window.estado == 'AGREGAR':
                misDatos = (matricula, descripcion, disponibilidad)
                miConsulta = "INSERT INTO vehiculo (matricula, descripcion, disponibilidad) VALUES (?,?,?);"
                miCrud.Create(miConsulta, misDatos)
            elif main_window.estado == 'EDITAR':
                miConsulta = "UPDATE vehiculo SET matricula = ?, descripcion = ?, disponibilidad = ? WHERE Id_vehiculo = ?;"
                misDatos = (matricula, descripcion, disponibilidad, main_window.selectedId)
                miCrud.Update(miConsulta, (misDatos,))
            elif main_window.estado == 'ELIMINAR':
                miConsulta = "DELETE from vehiculo where Id_vehiculo=?;"
                misDatos = (main_window.selectedId,)
                miCrud.Delete(miConsulta, misDatos)
            self.readVehiculos(main_window, 0)
            main_window.lineEdit_matricula.clear()
            main_window.lineEdit_descripcionVehiculo.clear()
            main_window.checkBox_vehiculo.setChecked(False)
            main_window.estado = 'CONSULTAR'
            self.showVehiculos(main_window)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al guardar vehículo: {e}")

    def createVehiculos(self, main_window):
        """Prepara la interfaz para agregar un nuevo vehículo."""
        try:
            main_window.estado = 'AGREGAR'
            main_window.lineEdit_matricula.clear()
            main_window.lineEdit_matricula.setEnabled(True)
            main_window.lineEdit_matricula.setFocus()
            main_window.lineEdit_descripcionVehiculo.clear()
            main_window.lineEdit_descripcionVehiculo.setEnabled(True)
            main_window.checkBox_vehiculo.setChecked(False)
            main_window.checkBox_vehiculo.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al preparar alta de vehículo: {e}")

    def updateVehiculos(self, main_window):
        """Prepara la interfaz para editar un vehículo existente."""
        try:
            main_window.estado = 'EDITAR'
            main_window.selectedId = main_window.tablavehiculo.item(main_window.tablavehiculo.currentRow(), 0).text()
            main_window.lineEdit_matricula.setText(main_window.tablavehiculo.item(main_window.tablavehiculo.currentRow(), 1).text())
            main_window.lineEdit_descripcionVehiculo.setText(main_window.tablavehiculo.item(main_window.tablavehiculo.currentRow(), 2).text())
            disponibilidad = main_window.tablavehiculo.item(main_window.tablavehiculo.currentRow(), 3).text()
            main_window.checkBox_vehiculo.setChecked(disponibilidad == "Sí")
            main_window.lineEdit_matricula.setEnabled(True)
            main_window.lineEdit_matricula.setFocus()
            main_window.lineEdit_descripcionVehiculo.setEnabled(True)
            main_window.checkBox_vehiculo.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al preparar edición de vehículo: {e}")

    def deleteVehiculos(self, main_window):
        """Elimina un vehículo de la base de datos."""
        try:
            main_window.estado = 'ELIMINAR'
            conn = sqlite3.connect('pedidos.sqlite3')
            cursor = conn.cursor()
            main_window.selectedId = main_window.tablavehiculo.item(main_window.tablavehiculo.currentRow(), 0).text()
            cursor.execute('DELETE FROM vehiculo WHERE Id_vehiculo = ?', (main_window.selectedId,))
            conn.commit()
            conn.close()
            self.readVehiculos(main_window, 0)
            self.showVehiculos(main_window)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al eliminar vehículo: {e}")

    def doubleClicked_tabla(self, main_window):
        pass

    def clicked_tabla(self, main_window):
        pass

    def showVehiculos(self, main_window):
        """Muestra todos los vehículos en la tabla de la interfaz."""
        try:
            main_window.tablavehiculo.setColumnCount(4)
            main_window.tablavehiculo.setHorizontalHeaderLabels(["ID", "Matrícula", "Descripción", "Disponibilidad"])
            miCrud = CRUD()
            vehiculos = miCrud.Read("SELECT * FROM vehiculo;")
            main_window.tablavehiculo.setRowCount(0)
            for index, vehiculo1 in enumerate(vehiculos):
                main_window.tablavehiculo.insertRow(index)
                main_window.tablavehiculo.setItem(index, 0, QTableWidgetItem(str(vehiculo1[0])))
                main_window.tablavehiculo.setItem(index, 1, QTableWidgetItem(vehiculo1[1]))
                main_window.tablavehiculo.setItem(index, 2, QTableWidgetItem(vehiculo1[2]))
                main_window.tablavehiculo.setItem(index, 3, QTableWidgetItem(str(vehiculo1[3])))
        except Exception as e:
            print(f"Error al mostrar vehículos: {e}")

"""f"""
