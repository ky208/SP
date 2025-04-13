/* Query */
use GroceryStore2222291;

--Query 1
SELECT cus.custName, s.store_Id, s.address 'Store Address', e2.empName 'Manager of the Store', co.created_at 'Transaction Date', i.brand, i.description, cod.quantity 'Quantity Purchased', e1.empName 'Served By'
FROM checkout co, checkoutDetails cod, customer cus, cashier cas, inventory inv, store s, item i, employee e1, employee e2,manager m
WHERE co.transaction_Id = cod.transaction_Id
AND cus.cust_Id = co.cust_Id
AND co.emp_Id = cas.emp_Id
AND cod.inventory_Id = inv.inventory_Id
AND inv.store_Id = s.store_Id
AND inv.item_Id = i.item_Id
AND cas.emp_Id = e1.emp_Id
AND s.store_Id = e2.storeRef_Id
AND e2.emp_Id = m.emp_Id

--Query 2
SELECT s.store_Id 'Store Manage ID', e.empName 'Name of Manager', e.storeRef_Id 'Store managed', inv.item_Id 'Item',inv.qtyInStock 'Quantity on inventory'
FROM inventory inv, store s, employee e, manager m
WHERE inv.store_Id = s.store_Id
AND s.store_Id = e.storeRef_Id
AND e.emp_Id = m.emp_Id

select * from employee
select * from manager

--Query 3

SELECT cus.custName 'Customer Name', SUM(cod.quantity) 'Quantity in Single Transaction'
FROM checkoutDetails cod, checkout co, customer cus
WHERE cod.transaction_Id = co.transaction_Id
AND co.cust_Id = cus.cust_Id
group by cus.custName,co.transaction_Id
HAVING sum(cod.quantity) <= 2

--Query 4

SELECT i.item_Id, i.description, (i.price * inv.qtyInStock) 'Retail',(i.cost * inv.qtyInStock) 'Wholesale',inv.qtyInStock, inv.store_Id
FROM inventory inv, item i
WHERE inv.item_Id = i.item_Id
AND inv.item_Id IN(SELECT item_Id FROM inventory GROUP BY item_Id HAVING COUNT(store_Id) >= 2)
ORDER BY item_Id

select * from inventory
select * from item
--Query 5

SELECT e1.emp_Id 'Employee ID',e1.empName 'Employee Name',e1.manager_Id 'Manager ID', e2.empName 'Manager Name'
FROM employee e1, employee e2
WHERE e1.manager_Id = e2.emp_Id


--Query 6

SELECT e1.empName 'Name of Manager',e2.emp_Id 'Boss ID', e1.emp_Id 'Manager ID',e2.empName 'Name of Boss', e1.storeRef_Id 'Store ID', s.address 'Address'
FROM employee e1,manager m,store s, employee e2
WHERE e1.manager_Id IN (SELECT emp_Id FROM employee where manager_Id IS NULL)
AND e1.emp_Id = m.emp_Id
AND s.store_Id = e1.storeRef_Id
AND e2.emp_Id = (SELECT emp_Id FROM employee where manager_Id IS NULL)


