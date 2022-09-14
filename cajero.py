from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from conexion import Conexion
from views.cajero import Ui_FrmCashier as CajeroMainWindow
from colorama import init, Fore, Back

from administrador import Administrador
from pago import Pagar
from pedidos import Pedidos
from views.frameMenu import Ui_Frame as FrameMenu

class CajeroWin(QMainWindow):
    def __init__(self,usuario):
        QMainWindow.__init__(self)
        self.cajeroUi = CajeroMainWindow()
        self.cajeroUi.setupUi(self)
        self.baseDatos = Conexion()
        self.usuario = usuario
        #self.cajeroUi.centralwidget.setStyleSheet("background-color:#363842;")
        self.cargar_privilegio(usuario)
        self.cargar_menu()
        self.iniciar_Lista()
        self.cajeroUi.BtnPagar.clicked.connect(self.botonPagar)
        self.cajeroUi.BtnAdmin.clicked.connect(self.botonAdmin)
        self.cajeroUi.BtnPedidosAnteriores.clicked.connect(self.botonPedidosAnteriores)
        self.show()

    #Aqui se habilita el boton de administrador si el usuario tiene privilegios
    def cargar_privilegio(self,usuario):
        nivel=self.baseDatos.privilegios(usuario)
        if nivel == "admin": self.cajeroUi.BtnAdmin.setVisible(True)
        else: self.cajeroUi.BtnAdmin.setVisible(False)
    
    #Esta funcion se encarga de cargar los widgets desde la base para ser mostados en el ScrollArea
    def cargar_menu(self):
        categoria,menu,precio=self.baseDatos.get_menu()
        #print(f"{categoria}\n{menu}\n{precio}") #DEBUG
        self.scrollLayout=QVBoxLayout()

        for y in range(len(categoria)):
            menuactual = []
            precioactual = []
            for x in range(len(menu)):
                if menu[x][1] == y+1:
                    #print("X es: ",menu[x]) #DEBUG
                    menuactual.append(menu[x][0])
                    precioactual.append(precio[x][0])
                
            self.categoria=QLabel()
            self.categoria.setStyleSheet("font-size:60px; background-color:#2aa9d5; padding: 5px 8px 5px 8px; font-family: 'Brush Script MT';")
            self.categoria.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.categoria.setText(f"{categoria[y]}")
            self.scrollLayout.addWidget(self.categoria)

            for x in range(len(menuactual)):
                articulo=Menu(menuactual[x],precioactual[x],self.cajeroUi.tableWidget,self.cajeroUi.lineTotal)
                self.scrollLayout.addWidget(articulo.productoWidget)

        self.cajeroUi.scrollAreaWidgetContents.setLayout(self.scrollLayout)
        #self.cajeroUi.scrollAreaWidgetContents.setStyleSheet("background-color:#6777cf")
        pass
    
    def cargar_menuAlter(self):
        pass

    #Aqui iniciamos la tabla y asignamos un nombre a las Cabeceras o Headers de la tabla
    def iniciar_Lista(self):
        self.cajeroUi.tableWidget.setColumnCount(4)
        self.cajeroUi.tableWidget.setStyleSheet("color:black;")
        self.cajeroUi.tableWidget.setHorizontalHeaderLabels(["Nombre del producto","Cantidad","Precio Unitario","Precio"])
        header=self.cajeroUi.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3,QHeaderView.ResizeMode.Stretch)
        self.cajeroUi.tableWidget.resizeRowsToContents()
        self.cajeroUi.BtnVaciar.clicked.connect(self.botonVaciar)

    def botonAdmin(self):
        self.admin = Administrador()
        #self.close()
        pass

    def botonPedidosAnteriores(self):
        self.pedidosWindow = Pedidos()
        pass

    def botonVaciar(self):
        self.cajeroUi.tableWidget.clearContents()
        self.cajeroUi.tableWidget.setRowCount(0)
        self.cajeroUi.lineTotal.setText("0")
        self.cajeroUi.lineEditNombrePedido.setText("")
        pass    
    
    def botonPagar(self):
        if self.cajeroUi.tableWidget.rowCount() == 0:
            msg=QMessageBox(QMessageBox.Icon.Warning,"No se ha añadido ningun producto","No se ha añadido ningun producto al pedido")
            msg.exec()
        else:
            pedido=self.generarOrden()
            self.pagar=Pagar(pedido,self.usuario,self.cajeroUi.lineEditNombrePedido.text())
            #self.close()
            pass

    def generarOrden(self)->list:
        pedido=list()
        rows=self.cajeroUi.tableWidget.rowCount()
        for x in range(rows):
            articulo=list()
            articulo.append(self.cajeroUi.tableWidget.item(x,0).text())
            articulo.append(self.cajeroUi.tableWidget.item(x,1).text())
            articulo.append(self.cajeroUi.tableWidget.item(x,2).text())
            articulo.append(self.cajeroUi.tableWidget.item(x,3).text())
            pedido.append(articulo)
        return pedido

class AlterMenu():
    def __init__(self,idProducto,tabla:QTableWidget,Total:QLineEdit):
        self.frameMenu = FrameMenu()
        self.frameMenu.setupUi()
        self.idProducto = idProducto
        self.Tabla = tabla
        self.Total = Total
        self.baseDatos = Conexion()
        self.producto = self.baseDatos.getproducto

    def boton(self):

        pass

    def actualizarDatos(self):
        pass

class Menu():
    def __init__(self,menuactual,precio,objeto:QTableWidget,Total:QLineEdit):
        self.menuactual=menuactual
        #print(Back.RED+str(self.id_p)+Back.RESET) #DEBUG
        self.objeto=objeto
        self.precio=precio
        self.total=Total
        self.productoWidget = QWidget()
        self.productoLayout = QHBoxLayout()
        self.productoWidget.setStyleSheet("background-color: #81c0d6;")
        self.productoWidget.setLayout(self.productoLayout)

        self.nombreProducto = QLabel()
        self.nombreProducto.setStyleSheet("background-color: #31a9d3; font-size: 18px;")
        self.nombreProducto.setText(f"{menuactual}")
        self.nombreProducto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nombreProducto.setFixedHeight(50)
        self.productoLayout.addWidget(self.nombreProducto)

        self.precioProducto = QLabel()
        self.precioProducto.setText(f"Precio: {precio} Bs.")
        self.precioProducto.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.precioProducto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.productoLayout.addWidget(self.precioProducto)

        self.spinCantidad=QSpinBox()
        self.spinCantidad.setStyleSheet("background-color: white; font-size: 18px;")
        self.spinCantidad.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.spinCantidad.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        self.spinCantidad.setFixedHeight(50)
        self.spinCantidad.setValue(1)
        self.productoLayout.addWidget(self.spinCantidad)

        self.botonAgregar = QPushButton()
        self.botonAgregar.setStyleSheet("background-color: #bddc42;")
        self.botonAgregar.setText("Agregar")
        self.botonAgregar.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Fixed)
        self.botonAgregar.setFixedSize(150,50)
        self.botonAgregar.clicked.connect(lambda:self.boton(self.menuactual,self.spinCantidad.text()))
        self.productoLayout.addWidget(self.botonAgregar)

    #Esta funcion agrega a la tabla el producto y su cantidad desde el cual se presionó el boton
    def boton(self,producto,cantidad):
        agregable=[producto,cantidad,str(self.precio),str(float(cantidad)*self.precio)]
        if int(cantidad) > 0:
            existe=self.comprobarExiste()
            if existe == -1:
                items=[]
                for pos,x in enumerate(agregable):
                    nuevoitem=QTableWidgetItem(x)
                    if pos != 1:
                        nuevoitem.setFlags(Qt.ItemFlag.ItemIsEditable)                        
                    items.append(nuevoitem)
                    
                
                self.objeto.setRowCount(self.objeto.rowCount()+1)
                self.objeto.cellChanged.connect(lambda:self.actualizarDatos())
                self.objeto.blockSignals(True)
                for pos,x in enumerate(items):
                    self.objeto.setItem(self.objeto.rowCount()-1,pos,x)
                self.objeto.blockSignals(False)
                self.actualizarTotal()
                #self.objeto.cellChanged(self.objeto.rowCount()-1,1).
            else:
                self.objeto.blockSignals(True)
                alterCantidad=self.objeto.item(existe,1).text()
                alterCantidad=int(alterCantidad)
                alterCantidad+=int(agregable[1])
                alterCantidad=QTableWidgetItem(str(alterCantidad))

                alterTotal=QTableWidgetItem(str(float(alterCantidad.text())*float(agregable[2])))
                alterTotal.setFlags(Qt.ItemFlag.ItemIsEditable)

                self.objeto.setItem(existe,1,alterCantidad)
                self.objeto.setItem(existe,3,alterTotal)
                self.objeto.blockSignals(False)
                self.actualizarTotal()
    
    #Esta funcion modifica el total si es que se modifico desde la tabla la cantidad de objetos
    #Tambien puede eliminar un objeto si su cantidad es 0
    def actualizarDatos(self):
        self.objeto.blockSignals(True)
        rows=self.objeto.rowCount()
        vacio=None
        for x in range(rows):
            cantidad = self.objeto.item(x,1)#aqui esta el total de ese producto
            cantidad = int(cantidad.text())
            precio = float(self.objeto.item(x,2).text())
            total = QTableWidgetItem(str(cantidad*precio))
            self.objeto.setItem(x,3,total)
            if cantidad == 0:
                vacio=x
        if vacio != None: self.objeto.removeRow(vacio)
        self.objeto.blockSignals(False)
        self.actualizarTotal()

    #Esta funcion comprueba si el item al que pertenece este widget ya ha sido agregado, si lo ha sido retorna su posicion y si no, retorna -1
    def comprobarExiste(self)->bool:
        for x in range(self.objeto.rowCount()):
            res = self.objeto.item(x,0)
            res=res.text()
            if res == self.menuactual:
                return x
        return -1

    def actualizarTotal(self):
        total=0
        rows = self.objeto.rowCount()
        for x in range(rows):
            total += float(self.objeto.item(x,3).text())
        self.total.setText(str(total))
        pass

