create database NEGOCIOBD;
use NEGOCIOBD;

create table Usuario(
	Id_usuario int not null auto_increment,
    Nombre varchar(30) not null,
    Apellido_pat varchar(30) not null,
    Apellido_mat varchar(30) not null,
    User_name varchar(30) not null,
    Contrasena varchar(256) not null,
    Nivel varchar(30),
    primary key(Id_usuario)
);

create table Tipos(
	Id_tipo int not null auto_increment,
    Nombre_tipo varchar(30),
    primary key(Id_tipo)
);

create table Menu(
	Id_producto int not null auto_increment,
    Id_tipo int not null,
    Nombre_producto varchar(30) not null,
    Precio float not null,
    primary key(Id_producto),
    foreign key(Id_tipo) references Tipos(Id_tipo)
);

create table Orden(
	Id_orden int not null auto_increment,
    Id_usuario int not null,
    Nombre_cliente varchar(30),
    Fecha datetime not null,
    Met_pago varchar(30) not null,
    primary key(Id_orden),
    foreign key(Id_usuario) references Usuario(Id_usuario)
);

create table Productos_pedidos(
	Id_orden int not null,
	Id_producto int not null,
    Cantidad int not null,
    foreign key(Id_orden) references Orden(Id_orden),
    foreign key(Id_producto) references Menu(Id_producto)
);



#drop database negociobd;
