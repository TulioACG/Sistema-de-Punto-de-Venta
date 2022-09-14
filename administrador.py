from PyQt5.QtWidgets import *
from conexion import Conexion
from views.administrador import Ui_MainWindow as AdminMainWindow
from colorama import init, Fore, Back

class Administrador(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.AdminUi = AdminMainWindow()
        self.AdminUi.setupUi(self)
        self.baseDatos = Conexion()
        self.conexionBotones()
        self.show()
        pass

    def conexionBotones(self):
        self.cambiarPestana(0)
        #Aqui definimos el ancho de los encabezados de las tablas que hay en las opciones para eliminar
        self.AdminUi.tablaEliminarProducto.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.AdminUi.tablaEliminarTipoProducto.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.AdminUi.tableEliminarUsuario.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.AdminUi.label_2.setText("Usuario: TulioACG")
        self.AdminUi.btnCerrar.clicked.connect(self.botonCerrar)
        
        #Aqui estan las conexiones con los botones
        self.AdminUi.btnAgregarUsuario.clicked.connect(lambda:self.cambiarPestana(1))
        self.AdminUi.btnAddUserConfirmar.clicked.connect(self.botonConfirmarAgregarUsuario)
        self.AdminUi.btnAddUserCancelar.clicked.connect(self.botonCancelarAgregarUsuario)

        self.AdminUi.BtnAgregarProducto.clicked.connect(lambda:self.cambiarPestana(2))
        self.AdminUi.btnConfirmarAgregarProducto.clicked.connect(self.botonConfirmarAgregarProducto)
        self.AdminUi.btnCancelarAgregarProducto.clicked.connect(self.botonCancelarAgregarProducto)
        self.llenarCategoria()

        self.AdminUi.BtnAgregarTipoP.clicked.connect(lambda:self.cambiarPestana(3))
        self.AdminUi.btnConfirmarAgregarTipoProducto.clicked.connect(self.botonConfirmarAgregarTipoProducto)
        self.AdminUi.btnCancelarAgregarTipoProducto.clicked.connect(self.botonCancelarAgregarTipoProducto)

        self.AdminUi.btnModUser.clicked.connect(lambda:self.cambiarPestana(4))
        self.AdminUi.btnConfirmarModUsuario.clicked.connect(self.botonConfirmarModUsuario)
        self.AdminUi.btnCancelarModUsuario.clicked.connect(self.botonCancelarModUsuario)
        self.tuplaUsuarios = self.llenarComboModUsuarios()
        self.llenarModUsuarios()
        self.AdminUi.comboBuscarUsuario.currentIndexChanged.connect(self.llenarModUsuarios)

        self.AdminUi.btnModProc.clicked.connect(lambda:self.cambiarPestana(5))
        self.AdminUi.comboBuscarProducto.currentIndexChanged.connect(self.llenarModProductoCasillas)
        self.llenarModProducto()
        self.AdminUi.btnCancelarModProducto.clicked.connect(self.botonCancelarModProducto)
        self.AdminUi.btnConfirmarModProducto.clicked.connect(self.botonConfirmarModProducto)

        self.AdminUi.btnModTipoP.clicked.connect(lambda:self.cambiarPestana(6))
        self.AdminUi.btnConfirmarModTipoP.clicked.connect(self.botonConfirmarModTipoProducto)
        self.AdminUi.btnCancelarModTipoP.clicked.connect(self.botonCancelarModTipoProducto)
        self.llenarBuscarTipoProducto()
        self.AdminUi.comboBuscarTipoProducto.currentIndexChanged.connect(self.llenarModTipoProducto)

        
        self.AdminUi.btnEliminarUsuario.clicked.connect(lambda:self.cambiarPestana(7))
        self.llenarTablaEliminarUsuario()
        self.AdminUi.btnActualizarTabla.clicked.connect(self.botonActualizarTablaEliminarUsuario)
        self.AdminUi.btnConfirmarEliminarUsuario.clicked.connect(self.botonConfirmarEliminarUsuario)
        self.AdminUi.btnCancelarEliminarUsuario.clicked.connect(self.botonCancelarEliminarUsuario)


        self.AdminUi.btnEliminarProducto.clicked.connect(lambda:self.cambiarPestana(8))
        self.llenarTablaEliminarProducto()
        self.AdminUi.btnActualizarEliminarProducto.clicked.connect(self.botonActualizarTablaEliminarProducto)
        self.AdminUi.btnCancelarEliminarProducto.clicked.connect(self.botonCancelarEliminarProducto)
        self.AdminUi.btnConfirmarEliminarProducto.clicked.connect(self.botonConfirmarEliminarProducto)

        self.AdminUi.btnEliminarTipoProducto.clicked.connect(lambda:self.cambiarPestana(9))
        self.llenarTablaEliminarTipoProducto()
        self.AdminUi.btnActualizarEliminarTipoProducto.clicked.connect(self.botonActualizarEliminarTipoProducto)
        self.AdminUi.btnCancelarEliminarTipoProducto.clicked.connect(self.botonCancelarEliminarTipoProducto)
        self.AdminUi.btnConfirmanEliminarTipoProducto.clicked.connect(self.botonConfirmarEliminarTipoProducto)
    
    def llenarTablaEliminarTipoProducto(self):
        tipoProductos = self.baseDatos.getTiposDeProductos()
        self.AdminUi.tablaEliminarTipoProducto.setRowCount(len(tipoProductos))
        for pos,x in enumerate(tipoProductos):
            self.AdminUi.tablaEliminarTipoProducto.setItem(pos,0,QTableWidgetItem(str(x[0])))
            self.AdminUi.tablaEliminarTipoProducto.setItem(pos,1,QTableWidgetItem(str(x[1])))

    def botonActualizarEliminarTipoProducto(self):
        self.AdminUi.tablaEliminarTipoProducto.clearContents()
        self.AdminUi.tablaEliminarTipoProducto.setRowCount(0)
        self.AdminUi.lineIDEliminarTipoProducto.setText("")
        self.llenarTablaEliminarTipoProducto()
    
    def botonConfirmarEliminarTipoProducto(self):
        idtipoProducto = self.AdminUi.lineIDEliminarTipoProducto.text()
        try:
            self.baseDatos.eliminarTipoDeProducto(idtipoProducto)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","Se ha eliminado con exito el tipo de producto")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al eliminar el tipo de producto\n\n"+str(ex))
            msg.exec()
        pass

    def botonCancelarEliminarTipoProducto(self):
        self.botonActualizarEliminarTipoProducto()
        self.cambiarPestana(0)

    def llenarTablaEliminarProducto(self):
        productos = self.baseDatos.getProductos()
        for x in productos:
            row = self.AdminUi.tablaEliminarProducto.rowCount()
            self.AdminUi.tablaEliminarProducto.insertRow(row)
            self.AdminUi.tablaEliminarProducto.setItem(row,0,QTableWidgetItem(str(x[0])))
            tipoProducto = self.baseDatos.getTipoFromID(x[1])
            self.AdminUi.tablaEliminarProducto.setItem(row,1,QTableWidgetItem(tipoProducto))
            self.AdminUi.tablaEliminarProducto.setItem(row,2,QTableWidgetItem(str(x[2])))
            self.AdminUi.tablaEliminarProducto.setItem(row,3,QTableWidgetItem(str(x[3])))

    def botonActualizarTablaEliminarProducto(self):
        self.AdminUi.tablaEliminarProducto.clearContents()
        self.AdminUi.tablaEliminarProducto.setRowCount(0)
        self.llenarTablaEliminarProducto()

    def botonConfirmarEliminarProducto(self):
        idProducto = self.AdminUi.lineEliminarProducto.text()
        try:
            self.baseDatos.eliminarProducto(idProducto)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","Se ha eliminado con exito al Producto")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al eliminar el producto\n\n"+str(ex))
            msg.exec()
        self.botonCancelarEliminarProducto()

    def botonCancelarEliminarProducto(self):
        self.cambiarPestana(0)
        self.AdminUi.lineEliminarProducto.setText("")
        self.botonActualizarTablaEliminarProducto()

    def botonActualizarTablaEliminarUsuario(self):
        self.AdminUi.tableEliminarUsuario.clearContents()
        self.AdminUi.tableEliminarUsuario.setRowCount(0)
        self.llenarTablaEliminarUsuario()

    def botonCancelarEliminarUsuario(self):
        self.botonActualizarTablaEliminarUsuario()
        self.AdminUi.lineIDUsuarioEliminar.setText("")
        self.cambiarPestana(0)

    def botonConfirmarEliminarUsuario(self):
        idUsuario = self.AdminUi.lineIDUsuarioEliminar.text()
        try:
            self.baseDatos.eliminarUsuario(idUsuario)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","Se ha eliminado con exito al usuario")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al eliminar al usuario\n\n"+str(ex))
            msg.exec()
        self.botonCancelarEliminarUsuario()

    def llenarTablaEliminarUsuario(self):
        usuario = self.baseDatos.getUsuarios()
        for x in usuario:
            row = self.AdminUi.tableEliminarUsuario.rowCount()
            self.AdminUi.tableEliminarUsuario.insertRow(row)
            for pos, y in enumerate(x):
                item = QTableWidgetItem(str(y))
                self.AdminUi.tableEliminarUsuario.setItem(row,pos,item)

    def llenarBuscarTipoProducto(self):
        self.AdminUi.comboBuscarTipoProducto.blockSignals(True)
        self.TipoProducto = self.baseDatos.getTiposDeProductos()
        self.AdminUi.comboBuscarTipoProducto.clear()
        for x in self.TipoProducto:
            self.AdminUi.comboBuscarTipoProducto.addItem(str(x[1]))
        self.AdminUi.comboBuscarTipoProducto.blockSignals(False)
        self.llenarModTipoProducto()

    def llenarModTipoProducto(self):
        currentIndex = self.AdminUi.comboBuscarTipoProducto.currentIndex()
        self.AdminUi.lineIDProductoMod.setText(str(self.TipoProducto[currentIndex][0]))
        self.AdminUi.lineModNombreTipoProducto.setText(self.TipoProducto[currentIndex][1])
    
    def botonConfirmarModTipoProducto(self):
        tipoProductoID = self.AdminUi.lineIDProductoMod.text()
        #tipoProductoID = self.baseDatos.getTipoID(tipoProductoID)
        nombre = self.AdminUi.lineModNombreTipoProducto.text()
        try:
            self.baseDatos.updateTipoDeProducto(tipoProductoID,nombre)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","¡¡¡Se ha actualizado con exito el tipo de producto!!!")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Se ha producido un error al actualizar el tipo de producto\n\n"+str(ex))
            msg.exec()
        self.botonCancelarModTipoProducto()

    def botonCancelarModTipoProducto(self):
        self.cambiarPestana(0)
        self.llenarBuscarTipoProducto()

    def llenarModProductoCasillas(self):
        currentIndex = self.AdminUi.comboBuscarProducto.currentIndex()
        self.AdminUi.lineIDproducto.setText(str(self.listaProductos[currentIndex][0]))
        indice = self.listaProductos[currentIndex][1]
        indice = self.baseDatos.getTipoFromID(indice)
        indice = self.AdminUi.comboModTipoProducto.findText(indice)
        self.AdminUi.comboModTipoProducto.setCurrentIndex(indice)
        self.AdminUi.lineModNombreProducto.setText(self.listaProductos[currentIndex][2])
        self.AdminUi.lineModPrecio.setText(str(self.listaProductos[currentIndex][3]))
    
    def llenarModProducto(self):
        self.AdminUi.comboBuscarProducto.blockSignals(True)
        self.AdminUi.comboBuscarProducto.clear()
        self.AdminUi.comboModTipoProducto.clear()
        self.listaProductos = self.baseDatos.getProductos()
        for x in self.listaProductos:
            producto = x[2]+" | Precio: "+str(x[3])
            self.AdminUi.comboBuscarProducto.addItem(producto)
        productos = self.baseDatos.getTipos()
        for x in productos:
            self.AdminUi.comboModTipoProducto.addItem(x[1])
        self.AdminUi.comboBuscarProducto.blockSignals(False)
        self.llenarModProductoCasillas()

    def botonConfirmarModProducto(self):
        idProducto = self.AdminUi.lineIDproducto.text()
        idTipoProducto = self.AdminUi.comboModTipoProducto.currentText()
        idTipoProducto = self.baseDatos.getTipoID(idTipoProducto)
        nombre = self.AdminUi.lineModNombreProducto.text()
        precio =  self.AdminUi.lineModPrecio.text()
        try:
            self.baseDatos.updateMenu(idProducto,idTipoProducto,nombre,precio)
            msg = QMessageBox(QMessageBox.Icon.Information,"Éxito","¡¡¡Se ha actualizado con exito la informacion del producto!!!")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al actualizar la informacion del producto: \n\n"+str(ex))
            msg.exec()
        self.botonCancelarModProducto()

    def botonCancelarModProducto(self):
        self.llenarModProducto()
        self.cambiarPestana(0)
    
    def llenarModUsuarios(self):
        self.AdminUi.comboBuscarUsuario.blockSignals(True)
        currentIndex = self.AdminUi.comboBuscarUsuario.currentIndex()
        self.AdminUi.lineIDusuario.setText(str(self.tuplaUsuarios[currentIndex][0]))
        self.AdminUi.lineModNombreUsuario.setText(self.tuplaUsuarios[currentIndex][1])
        self.AdminUi.lineModApellidoP.setText(self.tuplaUsuarios[currentIndex][2])
        self.AdminUi.lineModApellidoM.setText(self.tuplaUsuarios[currentIndex][3])
        self.AdminUi.lineModUserName.setText(self.tuplaUsuarios[currentIndex][4])
        if self.tuplaUsuarios[currentIndex][5] == "admin": self.AdminUi.comboModNivelAcceso.setCurrentIndex(1)
        else: self.AdminUi.comboModNivelAcceso.setCurrentIndex(0)
        self.AdminUi.comboBuscarUsuario.blockSignals(False)

    def llenarComboModUsuarios(self):
        self.AdminUi.comboBuscarUsuario.blockSignals(True)
        self.AdminUi.comboBuscarUsuario.clear()
        tuplaUsuarios = self.baseDatos.getUsuarios()
        for x in tuplaUsuarios:
            usuario = x[1]+" "+x[2]+" "+x[3]+" | Usuario: "+x[4]+" | Nivel: "+x[5]
            self.AdminUi.comboBuscarUsuario.addItem(usuario)
        self.AdminUi.comboBuscarUsuario.blockSignals(False)
        return tuplaUsuarios

    def botonConfirmarModUsuario(self):
        idUsuario = self.AdminUi.lineIDusuario.text()
        nombre = self.AdminUi.lineModNombreUsuario.text()
        apellidoPaterno = self.AdminUi.lineModApellidoP.text()
        apellidoMaterno = self.AdminUi.lineModApellidoM.text()
        userName = self.AdminUi.lineModUserName.text()
        contrasena = self.AdminUi.lineModContrasena.text()
        if contrasena == "": contrasena = self.baseDatos.getContrasena(idUsuario)
        nivel = self.AdminUi.comboModNivelAcceso.currentText()
        try:
            self.baseDatos.updateUsuario(idUsuario,nombre,apellidoPaterno,apellidoMaterno,userName,contrasena,nivel)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","¡¡Se ha actualizado con exito la informacion del usuario!!")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Information,"Error","Ha ocurrido un error al actualizar la informacion del usuario: \n\n"+str(ex))
            msg.exec()
        self.botonCancelarModUsuario()

    def botonCancelarModUsuario(self):
        self.tuplaUsuarios = self.llenarComboModUsuarios()
        self.llenarModUsuarios()
        self.cambiarPestana(0)

    def botonConfirmarAgregarTipoProducto(self):
        nombre = self.AdminUi.lineAgregarNombreTipoP.text()
        try:
            self.baseDatos.nuevoTipoProducto(nombre)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","Se ha añadido con exito el nuevo tipo de producto")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al crear el nuevo tipo de producto\n"+str(ex))
            msg.exec()
        self.botonCancelarAgregarTipoProducto()

    def botonCancelarAgregarTipoProducto(self):
        self.AdminUi.lineAgregarNombreTipoP.setText("")
        self.cambiarPestana(0)

    def llenarCategoria(self):
        listaCategorias = self.baseDatos.getTipos()
        for x in listaCategorias:
            self.AdminUi.comboCategoria.addItem(x[1])

    def botonConfirmarAgregarProducto(self):
        tipoProducto = self.AdminUi.comboCategoria.currentText()
        nombreProducto = self.AdminUi.lineNombreProducto.text()
        Precio = self.AdminUi.linePrecio.text()
        try:
            self.baseDatos.nuevoProducto(tipoProducto,nombreProducto,Precio)
            msg = QMessageBox(QMessageBox.Icon.Information,"Exito","¡¡Se ha añadido correctamente el Producto!!")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al crear el producto, por favor verifique sus datos\n"+str(ex))
            msg.exec()
        self.botonCancelarAgregarProducto()
    
    def botonCancelarAgregarProducto(self):
        self.AdminUi.lineNombreProducto.setText("")
        self.AdminUi.linePrecio.setText("")
        self.cambiarPestana(0)

    def cambiarPestana(self,numero:int):
        self.AdminUi.stackedWidget.setCurrentIndex(numero)

    def volverInicio(self):
        self.AdminUi.stackedWidget.setCurrentIndex(0)

    def botonConfirmarAgregarUsuario(self):
        nombre = self.AdminUi.lineNombre.text()
        apellidoPaterno = self.AdminUi.lineApellidoP.text()
        apellidoMaterno = self.AdminUi.lineApellidoM.text()
        user_name = self.AdminUi.lineUserName.text()
        password = self.AdminUi.lineContrasena.text()
        nivelAcceso = self.AdminUi.comboNivel.currentText()
        try:
            self.baseDatos.nuevoUsuario(nombre,apellidoPaterno,apellidoMaterno,user_name,password,nivelAcceso)
            msg=QMessageBox(QMessageBox.Icon.Information,"Exito","¡¡Se añadido correctamente el usuario!!")
            msg.exec()
        except Exception as ex:
            msg=QMessageBox(QMessageBox.Icon.Critical,"Error","Ha ocurrido un error al crear el usuario, revise por favor sus datos\n"+str(ex))
            msg.exec()
        self.botonCancelarAgregarUsuario()
        self.botonCancelarModUsuario()

    def botonCancelarAgregarUsuario(self):
        self.AdminUi.lineNombre.setText("")
        self.AdminUi.lineApellidoP.setText("")
        self.AdminUi.lineApellidoM.setText("")
        self.AdminUi.lineUserName.setText("")
        self.AdminUi.lineContrasena.setText("")
        self.AdminUi.comboNivel.setCurrentIndex(0)
        self.volverInicio()

    def botonCerrar(self):
        self.close()
