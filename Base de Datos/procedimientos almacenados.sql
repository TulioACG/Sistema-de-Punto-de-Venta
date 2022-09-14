use negociobd;
#-------------------------------------------------------------------------------------------------------
delimiter //
create procedure insertar_menu(in id_tipo int, in nombre varchar(30), in precio float)
begin
	insert into menu(Id_tipo,Nombre_producto,Precio) values(id_tipo,nombre,precio);
end //
delimiter ;

delimiter //
create procedure actualizar_menu(in idproducto int, in id_tipo int, in nombre varchar(30), in precio float)
begin
	update menu set Id_tipo = id_tipo, Nombre_producto = nombre, Precio = precio
	where Id_producto = idproducto;
end//
delimiter ;

delimiter //
create procedure eliminar_menu(in idproducto int)
begin
	delete from menu
    where Id_producto = idproducto;
end//
delimiter ;
#-------------------------------------------------------------------------------------------------------
delimiter //
create procedure insertar_orden(in id_usuario int, in nombre varchar(30),in fecha datetime, in met_pago varchar(30))
begin
	insert into orden(Id_usuario,Nombre_cliente,Fecha,Met_pago) values(id_usuario, nombre, fecha, met_pago);
end//
delimiter ;

delimiter //
create procedure actualizar_orden(in idorden int, in nombre varchar(30),in fecha datetime, in met_pago varchar(30))
begin
	update orden set Nombre_cliente=nombre, Fecha=fecha, Met_pago=met_pago
	where Id_orden = idorden;
end
//delimiter ;

delimiter //
create procedure eliminar_orden(in idorden int)
begin
	delete from orden
    where Id_orden = idorden;
end
//delimiter ;
#-------------------------------------------------------------------------------------------------------

delimiter //
create procedure insertar_productos_pedidos(in id_orden int, in id_producto int, in cantidad int)
begin
	insert into productos_pedidos(Id_orden,Id_producto,Cantidad) values(id_orden,id_producto,cantidad);
end
//delimiter ;

delimiter //
create procedure actualizar_productos(in idorden int, in id_producto int, in cantidad int)
begin
	update productos_pedidos set Id_producto=id_producto, Cantidad=cantidad
    where Id_orden = idorden;
end
// delimiter ;

delimiter //
create procedure eliminar_productos(in idorden int, in id_producto int)
begin
	delete from productos_pedidos
    where Id_orden = id_orden and Id_producto = idproducto;
end
// delimiter ;
#-------------------------------------------------------------------------------------------------------
delimiter //
create procedure insertar_tipos(in nombre varchar(30))
begin
	insert into tipos(Nombre_tipo) values(nombre);
end
// delimiter ;

delimiter //
create procedure actualizar_tipos(in idtipo int, in nombre varchar(30))
begin
	update tipos set Nombre_tipo = nombre
    where Id_tipo = idtipo;
end
// delimiter ;

delimiter //
create procedure eliminar_tipos(in idtipo int)
begin
	delete from tipos
    where Id_tipo = idtipo;
end
// delimiter ;
#-------------------------------------------------------------------------------------------------------
delimiter //
create procedure isertar_usuario(in nombre varchar(30), in apellido_pat varchar(30), in apellido_mat varchar(30), in user_name varchar(30), in contrasena varchar(256),in nivel varchar(30))
begin
	insert into usuario(Nombre, Apellido_pat, Apellido_mat, User_name, Contrasena,Nivel) values(nombre,apellido_pat,apellido_mat,user_name,contrasena,nivel);
end
// delimiter ;

delimiter //
create procedure actualizar_usuario(in idusuario int, in nombre varchar(30), in apellido_pat varchar(30), in apellido_mat varchar(30), in user_name varchar(30), in contrasena varchar(30),in nivel varchar(30))
begin
	update usuario 
    set Nombre = nombre, Apellido_pat = apellido_pat, Apellido_mat = apellido_mat, User_name = user_name, Contrasena = contrasena, Nivel = nivel 
    where Id_usuario = idusuario;
end
// delimiter ;

delimiter //
create procedure eliminar_usuario(in idusuario int)
begin
	delete from usuario
    where Id_usuario = idusuario;
end
// delimiter ;
#-------------------------------------------------------------------------------------------------------
/*
delimiter //
create function login_usuario(usuario varchar(30), contrasena varchar(256))
	RETURNS BOOL
    NOT DETERMINISTIC
    READS SQL DATA
begin
	return exists(select Nombre from usuario where User_name = usuario and Contrasena = contrasena);
end
// delimiter ;*/

