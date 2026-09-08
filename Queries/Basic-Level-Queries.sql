select name,price from products; -- 1
select name,price from products where price>5000 order by price asc; -- 2
select name,price from products where price between 1000 and 5000 order by price asc; -- 3
select name,price as Expensive from products order by Expensive desc  limit 10;-- 4
select name,price as Low_Cost from products order by Low_Cost asc limit 10;-- 5
select concat(first_name,last_name) as Name from customers where first_name like "A%";-- 6
select concat(first_name,last_name) as Name from customers where last_name like "%n";-- 7
select name from products where name like "%phone%";-- 8
select  distinct order_id,status from orders order by status ;-- 9
select payment_method from payments ;-- 10
select o.order_id,s.status from orders as o inner join shipments as s on o.order_id=s.order_id where s.status="SHIPPED" or s.status="DELIVERED";-- 11
select name,price from products where (price=999) or (price=1999) or (price=2999);-- 12
select *  from customers where customer_id between 1000 and 1100;-- 13
select * from customers order by created_at desc limit 20;-- 14
select  * from products order by name asc;-- 15
select name,stock_quantity from products where stock_quantity<50;-- 16
select name,stock_quantity from products where stock_quantity between 100 and 500;-- 17
select * from orders where total_amount>10000 order by total_amount desc;-- 18
select * from customers where email like "%gmail%";-- 19
select name,description from products where description is null;-- 20 

