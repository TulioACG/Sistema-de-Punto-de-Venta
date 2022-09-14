from PyQt5.QtWidgets import *
from views import imagenes
import sys

from administrador import Administrador
from pago import Pagar
from cajero import CajeroWin, Menu
from login import LoginWin


if __name__ == "__main__":
    #Aqui es donde se ejecuta el programa cargando el "formulario" de login
    app=QApplication(sys.argv)
    #window=LoginWin()
    window=CajeroWin("TulioACG")
    #window=Pagar()
    sys.exit(app.exec_())