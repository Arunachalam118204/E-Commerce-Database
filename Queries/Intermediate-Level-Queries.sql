select c.customer_id,concat(c.first_name,c.last_name) as Fullname,o.total_amount as Spend_Amount
from customers as c 
inner join orders as o 
		on c.customer_id=o.customer_id;  -- 1

select c.customer_id,concat(c.first_name,c.last_name) as Fullname, count(osh.order_id) as OrderCount 
from customers as c inner join orders as o 
		on c.customer_id=o.customer_id 
inner join order_status_history as osh 
		on o.order_id=osh.order_id group by c.customer_id having OrderCount>2; -- 2

select c.*,o.total_amount from customers as c inner join orders as o 
		on c.customer_id=o.customer_id 
		order by total_amount desc limit 10; -- 3

select count(o.order_id) as NumberofOrder ,osh.status from orders as o
inner join order_status_history as osh 
		on o.order_id=osh.order_id group by osh.status; -- 4

select AVG(total_amount) as AverageAmount,status from orders group by status; -- 5

select p.name,AVG(pr.rating) as Average_rating from products as p inner join product_reviews as pr
		on p.product_id=pr.product_id group by p.name; -- 6

select p.product_id,p.name,pr.rating from products as p inner join product_reviews as pr
		on p.product_id=pr.product_id where rating>3; -- 7

Select name,price from products order by price desc; -- 8

select p.product_id,p.name,sum(oi.quantity) as QuantityCount from products as p 
inner join order_items as oi 
		on p.product_id=oi.product_id
inner join orders as o 
		on o.order_id=oi.order_id
		group by p.product_id,p.name; -- 9

select p.name,sum(oi.quantity) as Quantity from products as p
inner join order_items as oi 
		on p.product_id=oi.product_id
		group by name order by Quantity desc limit 10; -- 10

select p.name,sum(oi.quantity*oi.unit_price) as Revenue from products as p
inner join order_items as  oi 
		on p.product_id=oi.product_id group by name; -- 11

select concat(c.first_name,c.last_name) as name,count(o.customer_id) as OrderCount from customers as c 
inner join orders as o 
		on c.customer_id=o.customer_id group by c.customer_id having OrderCount>1; -- 12

select concat(c.first_name,c.last_name) as name,count(o.customer_id) as OrderCount from customers as c 
inner join orders as o 
		on c.customer_id=o.customer_id group by c.customer_id having OrderCount is null; -- 13

select payment_method,count(payment_method) as CountofUsing from payments group by payment_method; -- 14

select o.order_id,concat(c.first_name,c.last_name) as Name ,total_amount as Amount ,payment_method,payment_status 
from orders as o
inner join customers as c 
		on o.customer_id=c.customer_id 
inner join payments as p 
		on o.order_id=p.order_id ; -- 15




