create database shopping_cart;
use shopping_cart;
create table products(id int auto_increment primary key,name varchar(100),price decimal(10,2),stock int);
create table orders(id int auto_increment primary key,customer_name varchar(100),total_amount decimal(10,2),order_date datetime default current_timestamp);
create table order_items(id int auto_increment primary key,
order_id int,product_id int,quantity int,price decimal(10,2),
foreign key(order_id) references orders(id),foreign key(id)references products(id));
insert into products(name,price,stock)
values('laptop',45000,10),
('mouse',500,20),
('keyboard',1200,15),
('monitor',12000,8);
