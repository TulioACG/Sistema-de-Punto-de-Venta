from PyQt5.QtWidgets import *
from conexion import Conexion
from views.login import Ui_MainWindow as loginMainWindow

from cajero import CajeroWin

class LoginWin(QMainWindow):
    def __init__(self):
        #esta seccion del codigo enlaza la vista con este controlador
        QMainWindow.__init__(self)
        self.loginUi = loginMainWindow()
        self.loginUi.setupUi(self)
        self.loginUi.pushButton.clicked.connect(self.btn_ingresar) #Aqui se conecta el boton ingresar con la funcion btn_ingresar
        self.baseDatos = Conexion()   #Esto es una instancia de la conexion con la base de datos
        self.show()

    #Esto es lo que ocurre al precionar el boton ingresar
    def btn_ingresar(self):
        usuario = self.loginUi.txtUsuario.text()          #Se captura el usuario en una variable
        contraseña = self.loginUi.txtPassword.text()      #se captura la contraseña en una variable
        verificacion = self.baseDatos.iniciar_sesion(usuario,contraseña)

        #Si el usuario y contraseña son validos se abrira la ventana del cajero
        if verificacion:
            self.cajero=CajeroWin(usuario)
            self.close()

        #Aqui se muestra un messagebox si es que no se han ingresado correctamente los credenciales
        else:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Los datos ingresados no son validos\npor favor verifique de nuevo")
            msg.exec()