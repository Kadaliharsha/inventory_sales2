create database inventorysales;
use inventorysales;
create table products(
	product_id varchar(10) primary key,
    name varchar(50),
    category varchar(50),
    price decimal(10,2),
    quantity int
);

create table customers(
	customer_id varchar(10) primary key,
    name varchar(50),
    phone varchar(10)
);

create table sales(
	sale_id int primary key auto_increment,
    customer_id varchar(10),
    product_id varchar(10),
    quantity int,
    sale_date date,
    foreign key(customer_id) references customers(customer_id),
    foreign key(product_id) references products(product_id)
);

select * from customers;
select * from products;
select * from sales;


