from views.pedidosAnteriores import Ui_MainWindow as PedidosMainWindow
from PyQt5.QtWidgets import *
from conexion import *
from views.framePedido import Ui_Frame

class Pedidos(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.pedidosUi = PedidosMainWindow()
        self.pedidosUi.setupUi(self)
        self.baseDatos = Conexion()
        self.pedidosUi.btnCerrar.clicked.connect(self.botonCerrar)
        self.pedidosUi.btnEliminarPedido.clicked.connect(self.botonEliminarPedido)
        self.llenarPedidosAnteriores()
        self.show()

    def llenarPedidosAnteriores(self):
        self.pedidosAnteriores = self.baseDatos.getPedidosAnteriores()
        self.pedidosAnteriores = self.pedidosAnteriores[::-1]
        self.pedidosUi.scrollAreaWidgetContents.setStyleSheet("QWidget{background-color:black;} QLineEdit{background-color:white;}")
        for x in self.pedidosAnteriores:
            self.pedidoItem = Contenido(x[0],x[2],x[4],self.pedidosUi.scrollAreaWidgetContents)
            separador = QWidget()
            separador.setMaximumHeight(30)
            separador.setMinimumHeight(30)
            self.pedidosUi.scrollAreaWidgetContents.layout().addWidget(separador)

    def botonCerrar(self):
        self.close()

    def actualizarDatos(self):
        self.pedidosUi.setupUi(self)
        self.pedidosUi.btnCerrar.clicked.connect(self.botonCerrar)
        self.pedidosUi.btnEliminarPedido.clicked.connect(self.botonEliminarPedido)
        self.llenarPedidosAnteriores()

    def botonEliminarPedido(self):
        pedidoID = self.pedidosUi.lineIDeliminarPedido.text()
        try:
            self.baseDatos.eliminarPedidoFromID(pedidoID)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","Se ha eliminado con exito el pedido")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al eliminar el pedido:\n\n"+str(ex))
            msg.exec()
        self.actualizarDatos()

class Contenido():
    def __init__(self,idPedido,NombrePedido,metPago,parent:QWidget):
        self.idPedido = idPedido
        self.nombrePedido = NombrePedido
        self.parent = parent
        self.metodoPado = metPago
        self.baseDatos = Conexion()
        self.llenarContenido()

    def obtenerProductosDelPedido(self):
        pedidoenbruto = self.baseDatos.getProductosDeOrdenFromID(self.idPedido)
        self.productosDelPedido = list()
        self.cantidadesDelPedido = list()
        self.preciosDelPedido = list()
        for x in pedidoenbruto:
            productoNombre = self.baseDatos.getProductoNameFromID(x[0])
            self.productosDelPedido.append(productoNombre)
            self.cantidadesDelPedido.append(x[1])
            precio = self.baseDatos.getPrecioFromID(x[0])
            self.preciosDelPedido.append(precio)

    def llenarTablaPedidos(self):
        cantidad = len(self.productosDelPedido)
        self.frameReal.tablaProductos.setRowCount(cantidad)
        self.totalGral = 0
        for pos,x in enumerate(self.productosDelPedido):
            item = QTableWidgetItem(str(x))
            self.frameReal.tablaProductos.setItem(pos,0,item)
            item = QTableWidgetItem(str(self.preciosDelPedido[pos]))
            self.frameReal.tablaProductos.setItem(pos,1,item)
            item = QTableWidgetItem(str(self.cantidadesDelPedido[pos]))
            self.frameReal.tablaProductos.setItem(pos,2,item)
            total = self.preciosDelPedido[pos] * self.cantidadesDelPedido[pos]
            self.totalGral+=total
            item = QTableWidgetItem(str(total))
            self.frameReal.tablaProductos.setItem(pos,3,item)
        self.frameReal.lineTotal.setText(str(self.totalGral))

    def llenarContenido(self):
        self.obtenerProductosDelPedido()
        self.frameContenedor =QFrame()
        self.frameReal = Ui_Frame()
        self.frameReal.setupUi(self.frameContenedor)
        self.frameReal.tablaProductos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.frameContenedor.setStyleSheet("""
        QFrame{
            background-color:#a8cbed;
            
        }
        QLabel{
            font-size:15px;
        }
        QTableWidget{
            background-color:white;
        }
        """)

        self.llenarTablaPedidos()
        self.frameReal.lineIDdelPedido.setText(str(self.idPedido))
        self.frameReal.lineNombreDelCliente.setText(self.nombrePedido)
        self.frameReal.lineMetodoPago.setText(self.metodoPado)
        self.parent.layout().addWidget(self.frameContenedor)