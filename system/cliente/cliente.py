import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit
from tools.DBCrud import CRUD
from PyQt5.QtCore import QDate

class cliente():
    """Clase especifidica de las Choferes """
    nombre_cliente=""
    cuit_cliente=""
    dni_cliente=""
    ciudad_cliente=""
    direccion_cliente=""
    tel_cliente=""
    
    def __init__ (self,nombre,cuit,dni,fn,tel,direccion):
        self.nombre=nombre_cliente
        self.cuit=cuit_cliente
        self.dni=dni_cliente
        self.ciudad=ciudad_cliente
        self.tel=tel_cliente
        self.direccion=direccion_cliente
        self.index=0
    
    def createClientes(self):
        self.estado='AGREGAR'
        self.lineEdit_nombre_cliente.clear()
        self.lineEdit_nombre_cliente.setEnabled(True) # activa el lineedit nombre
        self.lineEdit_nombre_cliente.setFocus() 
        self.lineEdit_cuit_cliente.clear()
        self.lineEdit_cuit_cliente.setEnabled(True) 
        self.dni_cliente.clear()
        self.lineEdit_dni.setEnabled(True)  
        self.editdate.setDate(QDate.currentDate())
        self.editdate.setEnabled(True)  
        self.lineEdit_direccion.clear()
        self.lineEdit_direccion.setEnabled(True)
        self.lineEdit_tel.clear()
        self.lineEdit_tel.setEnabled(True)  