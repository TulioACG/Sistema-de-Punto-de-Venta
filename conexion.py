from turtle import back
import mysql.connector
from datetime import datetime
import regex as re
from colorama import init,Fore,Back

init()

class Conexion():
    def __init__(self):
        self.conexion=mysql.connector.connect(
            user='root',
            password='08031998xd.ñ',
            host='localhost',
            port='3306',
            database='negociobd')

    def iniciar_sesion(self,usuario,contraseña)->bool:
        cur=self.conexion.cursor()
        sql = f"SELECT Nombre FROM  usuario WHERE User_name = BINARY '{usuario}' and Contrasena = BINARY '{contraseña}';"
        cur.execute(sql)
        userverification=cur.fetchall()
        cur.close()
        if len(userverification) == 1:
            return True
        else: return False

    def privilegios(self,usuario)->str:
        cur=self.conexion.cursor()
        sql= f"SELECT Nivel FROM usuario WHERE User_name = BINARY '{usuario}';"
        cur.execute(sql)
        nivel=cur.fetchone()
        cur.close()
        return nivel[0]

    def dividirListas(self,listaTuplas):
        resultado=list()
        for x in listaTuplas:
            for y in x:
                resultado.append(y)
        return list(resultado)

    def get_menu(self):
        cur=self.conexion.cursor()
        sql="select Nombre_tipo from tipos;"
        sql2="select Nombre_producto, Id_tipo from menu;"
        sql3="select Precio, Id_tipo from menu;"
        cur.execute(sql)
        categorias=self.dividirListas(cur.fetchall())
        cur.execute(sql2)
        menu=cur.fetchall()
        cur.execute(sql3)
        precios=cur.fetchall()
        cur.close()
        return categorias,menu,precios

    def crearOrden(self,nombrePedido,metPago,productos:list,cantidad:list,usuario):
        fecha=datetime.today()
        usuarioID=self.getUserID(usuario)
        cur=self.conexion.cursor()
        sql=f"CALL insertar_orden('{usuarioID}','{nombrePedido}','{fecha}','{metPago}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()
        self.insertarProductosOrden(fecha,productos,cantidad)

    def insertarProductosOrden(self,fecha,productos:list,cantidad:list):
        ordenID = self.getOrdenID(fecha)
        for pos,x in enumerate(productos):
            productoID = self.getProductoID(x)
            cur = self.conexion.cursor()
            sql = f"CALL insertar_productos_pedidos('{ordenID}','{productoID}','{cantidad[pos]}');"
            cur.execute(sql)
            self.conexion.commit()
            cur.close()

    def getProductoID(self,nombreProducto):
        cur=self.conexion.cursor()
        sql=f"SELECT Id_producto FROM menu WHERE Nombre_producto = '{nombreProducto}';"
        cur.execute(sql)
        productoID = cur.fetchall()
        productoID = self.dividirListas(productoID)[0]
        cur.close()
        return productoID

    def getOrdenID(self,fecha):
        cur=self.conexion.cursor()
        fecha=str(fecha)
        segundos=re.search("\d\d?\..*",fecha)[0]
        segundos=float(segundos)
        fecha = re.sub("\d\d?\..*",f"{int(round(segundos))}",str(fecha))
        sql=f"SELECT Id_orden FROM orden WHERE Fecha = '{fecha}';"
        cur.execute(sql)
        ordenID = cur.fetchall()
        ordenID = self.dividirListas(ordenID)[0]
        cur.close()
        return ordenID

    def getUserID(self,usuario)->int:
        cur=self.conexion.cursor()
        sql=f"SELECT Id_usuario FROM usuario WHERE User_name = '{usuario}';"
        cur.execute(sql)
        usuarioID=cur.fetchall()
        usuarioID=self.dividirListas(usuarioID)[0]
        cur.close()
        return usuarioID

    def nuevoUsuario(self,nombre,apellidoP,apellidoM,userName,contrasena,nivel):
        cur = self.conexion.cursor()
        sql = f"CALL isertar_usuario('{nombre}', '{apellidoP}', '{apellidoM}', '{userName}', '{contrasena}', '{nivel}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def nuevoProducto(self,tipoP,nombre,precio):
        idTipo = self.getTipoID(tipoP)
        cur = self.conexion.cursor()
        sql = f"CALL insertar_menu('{idTipo}','{nombre}','{precio}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def getTipoID(self,tipoP):
        cur = self.conexion.cursor()
        sql = f"select Id_tipo from tipos where Nombre_tipo = binary '{tipoP}';"
        cur.execute(sql)
        idTipo = cur.fetchone()[0]
        cur.close()
        return idTipo

    def getTipoFromID(self,tipoID):
        cur = self.conexion.cursor()
        sql = f"select Nombre_tipo from tipos where Id_tipo = '{tipoID}';"
        cur.execute(sql)
        tipoName = cur.fetchone()[0]
        cur.close()
        return tipoName

    def getTipos(self)->list:
        cur = self.conexion.cursor()
        sql = "select * from tipos;"
        cur.execute(sql)
        tipos = cur.fetchall()
        #tipos = self.dividirListas(tipos)
        cur.close()
        return tipos

    def nuevoTipoProducto(self,nombre):
        cur = self.conexion.cursor()
        sql = f"call insertar_tipos('{nombre}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def getUsuarios(self) -> list:
        cur = self.conexion.cursor()
        sql = f"select ID_usuario, Nombre, Apellido_pat, Apellido_mat, User_name, Nivel from usuario"
        cur.execute(sql)
        listaCategorias = cur.fetchall()
        cur.close()
        return listaCategorias

    def getContrasena(self,idUsuario):
        cur = self.conexion.cursor()
        sql = f"SELECT Contrasena FROM usuario WHERE Id_usuario = BINARY '{idUsuario}';"
        cur.execute(sql)
        contrasena = cur.fetchone()[0]
        cur.close()
        return contrasena

    def updateUsuario(self,idUsuario,nombre,apellidoP,apellidoM,userName,contrasena,nivel):
        cur = self.conexion.cursor()
        sql = f"CALL actualizar_usuario('{idUsuario}','{nombre}','{apellidoP}','{apellidoM}','{userName}','{contrasena}','{nivel}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def getProductos(self)->list:
        cur = self.conexion.cursor()
        sql = "select * from menu"
        cur.execute(sql)
        listaProductos = cur.fetchall()
        cur.close()
        return listaProductos

    def getTiposDeProductos(self)->list:
        cur = self.conexion.cursor()
        sql = "select * from tipos;"
        cur.execute(sql)
        tipoPLista = cur.fetchall()
        cur.close()
        return tipoPLista

    def getTipoProducto(self,idTipo):
        cur = self.conexion.cursor()
        sql = f"select Nombre_tipo from tipos where Id_tipo = '{idTipo}';"
        cur.execute(sql)
        tipoP = cur.fetchone()[0]
        cur.close()
        return tipoP

    def updateMenu(self,idProducto,idTipo,nombre,precio):
        cur = self.conexion.cursor()
        sql = f"CALL actualizar_menu('{idProducto}','{idTipo}','{nombre}','{precio}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def updateTipoDeProducto(self,idTipo,nombre):
        cur = self.conexion.cursor()
        sql = f"CALL actualizar_tipos('{idTipo}','{nombre}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def eliminarUsuario(self,idUsuario):
        cur = self.conexion.cursor()
        sql = f"CALL eliminar_usuario('{idUsuario}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def eliminarProducto(self, idProducto):
        cur = self.conexion.cursor()
        sql = f"CALL eliminar_menu('{idProducto}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def eliminarTipoDeProducto(self,idTipo):
        cur = self.conexion.cursor()
        sql = f"CALL eliminar_tipos('{idTipo}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()
    
    def getPedidosAnteriores(self)->list:
        cur = self.conexion.cursor()
        sql = "select * from orden"
        cur.execute(sql)
        pedidos = cur.fetchall()
        cur.close()
        return pedidos

    def getProductosDeOrdenFromID(self,idorden)->list:
        cur = self.conexion.cursor()
        sql = f"SELECT Id_producto, Cantidad FROM productos_pedidos WHERE Id_orden = '{idorden}';"
        cur.execute(sql)
        productos = cur.fetchall()
        cur.close()
        return productos

    def getProductoNameFromID(self,idProducto):
        cur = self.conexion.cursor()
        sql = f"SELECT Nombre_producto FROM menu WHERE Id_producto = '{idProducto}';"
        cur.execute(sql)
        producto = cur.fetchone()
        cur.close()
        if producto == None:
            return "no existe"
        return producto[0]

    def getPrecioFromID(self,idProducto):
        cur = self.conexion.cursor()
        sql = f"SELECT Precio FROM menu WHERE Id_producto = '{idProducto}';"
        cur.execute(sql)
        precio = cur.fetchone()[0]
        cur.close()
        return precio

    def eliminarPedidoFromID(self,pedidoID):
        self.eliminarProductosDePedido(pedidoID)
        cur = self.conexion.cursor()
        sql = f"CALL eliminar_orden('{pedidoID}');"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()

    def eliminarProductosDePedido(self,pedidoID):
        cur = self.conexion.cursor()
        sql = f"DELETE FROM productos_pedidos WHERE Id_orden = '{pedidoID}';"
        cur.execute(sql)
        self.conexion.commit()
        cur.close()
"""
prueba=Conexion()
prueba.getTipos()

prueba.getTipos()
prueba.getTipoID("Helados")
prueba.crearOrden("Juan perez","Efectivo",["Hamburguesa Doble","Hamburguesa Simple","Coca Cola 2L"],[2,1,1],"TulioACG")"""