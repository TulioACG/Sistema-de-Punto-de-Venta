from cgitb import text
from PyQt5.QtWidgets import *
from conexion import Conexion
from views.metodo_pago import Ui_FrmPagar as PagoMainWindow


class Pagar(QMainWindow):
    def __init__(self,datos:list,usuario,nombrepedido):
        #los "datos" recibidos son = lista[Nombre producto, Cantidad, Precio, total]
        QMainWindow.__init__(self)
        self.pagoUi = PagoMainWindow()
        self.pagoUi.setupUi(self)
        self.setFixedSize(794,527)
        self.datos=datos
        self.usuario=usuario
        self.nombrePedido = nombrepedido
        self.pagoUi.btnConfirmar.clicked.connect(self.botonConfirmar)
        self.pagoUi.btnCancelar.clicked.connect(self.botonCancelar)
        self.pagoUi.btnImprimir.clicked.connect(self.botonImprimir)
        self.llenarPedido()
        self.baseDatos=Conexion()
        self.show()

    def llenarPedido(self):
        self.pagoUi.lineEditNombrePedido.setText(self.nombrePedido)
        self.pagoUi.tableWidget.setColumnCount(4)
        self.pagoUi.tableWidget.setHorizontalHeaderLabels(["Nombre del producto","Cantidad","Precio Unitario","Precio Total"])
        header=self.pagoUi.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3,QHeaderView.ResizeMode.Stretch)
        rows=len(self.datos)
        for x in range(rows):
            self.pagoUi.tableWidget.insertRow(x)
            for y in range(len(self.datos[x])):
                self.pagoUi.tableWidget.setItem(x,y,QTableWidgetItem(str(self.datos[x][y])))
        total=0
        for x in range(len(self.datos)):
            total+=float(self.datos[x][3])
        self.pagoUi.lineEditTotal.setText(str(total))

    def generarListas(self):
        self.listaProductos = list()
        self.listaCantidades = list()
        rowcount = self.pagoUi.tableWidget.rowCount()
        for x in range(rowcount):
            item = self.pagoUi.tableWidget.item(x,0)
            item = item.text()
            self.listaProductos.append(item)

            item = self.pagoUi.tableWidget.item(x,1)
            item = item.text()
            self.listaCantidades.append(item)

    def botonConfirmar(self):
        nombre = self.pagoUi.lineEditNombrePedido.text()
        metPago = self.pagoUi.comboMetPago.currentText()
        usuario = self.usuario
        self.generarListas()
        try:
            self.baseDatos.crearOrden(nombre,metPago,self.listaProductos,self.listaCantidades,usuario)
            self.msg = QMessageBox(QMessageBox.Icon.Information,"Se ha añadido la orden","Se ha añadido la orden sin problemas")
            self.msg.exec()
        except Exception as ex:
            self.msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al añadir la orden\n\n"+str(ex))
            self.msg.exec()
        self.close()

    def botonCancelar(self):
        self.close()

    def getDatos(self)->str:
        rows=len(self.datos)
        texto = ""
        for x in range(rows):
            texto += str(self.datos[x][0]) + "\t\t" + str(self.datos[x][1]) + "\t\t" + str(self.datos[x][2]) + "\t\t" + str(self.datos[x][3]) +"\n"
        return texto

    def botonImprimir(self):
        from datetime import datetime
        total=0
        for x in range(len(self.datos)):
            total+=float(self.datos[x][3])

        texto = f"""
Sistema de Ventas
Carrera Ing de sistemas
Universidad Autonoma del Beni

----------------------------------------------

Cajero: {self.usuario}

Productos:
Producto\t\tCantidad\t\tPrecio\t\tTotal
{self.getDatos()}

TOTAL: {total} Bs.

----------------------------------------------

Fecha: {datetime.now()}

Trinidad-Beni-Bolivia
        """

        #print(texto)
        self.imrpimir = Imprimir(texto)
        pass

from views.FrameImprimir import Ui_Frame as FrameImprimir
from views import imagenes
class Imprimir():
    def __init__(self,texto):
        self.windoww = QFrame()
        self.windoww.setFixedSize(0,0)
        self.frameImprimir = FrameImprimir()
        self.frameImprimir.setupUi(self.windoww)
        self.texto = texto
        self.llenarDatos()
        self.windoww.show()

    def llenarDatos(self):
        self.frameImprimir.labelImprimir.setText(self.texto)