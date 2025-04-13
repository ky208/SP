--CREATE DATABASE GroceryStore2222291;
USE GroceryStore2222291;

-- Drop tables if they exist
DROP TABLE IF EXISTS checkoutDetails;
DROP TABLE IF EXISTS checkout;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS manager;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS dependent;
DROP TABLE IF EXISTS cashier;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS store;

--Creating Tables
CREATE TABLE store (	
store_Id int IDENTITY(1,1) Not Null,
address varchar(50) Not Null,
PRIMARY KEY (store_Id)
);


CREATE TABLE employee (
emp_Id int IDENTITY(1,1) Not Null,
storeRef_Id int Not Null,
manager_Id int Null,
empName varchar(50) Not Null,
username varchar(40) Null,
password varchar(40) Null,
SSN bigint Not Null,
email varchar(50) Not Null,
phone bigint Not Null,
empAddress varchar(50) Not Null,
payType int Not Null,
dateHired date Null,
dateStart date Not Null,
dateEnd date Null,
pay decimal(10,2) Not Null,
PRIMARY KEY (emp_Id),
FOREIGN KEY (storeRef_Id) REFERENCES store(store_Id),
FOREIGN KEY (manager_Id) REFERENCES employee(emp_Id),
);


CREATE TABLE manager (
emp_Id int Not Null,
director int Null,
PRIMARY KEY (emp_Id),
FOREIGN KEY (emp_Id) REFERENCES employee(emp_Id),
);

CREATE TABLE cashier (
emp_Id int Not Null,
lastPwChanged datetime default current_timestamp,
PRIMARY KEY (emp_Id),
FOREIGN KEY (emp_Id) REFERENCES employee(emp_Id)
);


CREATE TABLE dependent (
dependent_Id int IDENTITY(1,1) Not Null,
emp_Id int Not Null,
name varchar(50) Not Null,
relation varchar(50) Not Null,
PRIMARY KEY (dependent_Id),
FOREIGN KEY (emp_Id) REFERENCES employee(emp_Id),
);


CREATE TABLE item (
item_Id int IDENTITY(1,1) Not Null,
brand  varchar(50) Not Null,
description varchar(50) Not Null,
price decimal(10,2) Not Null,
cost decimal(10,2) Not Null,
shape varchar(50) Not Null,
size varchar(50) Not Null,
UPC bigint Not Null,
weight decimal(10,2) Not Null,
taxable int Not Null,
PRIMARY KEY (item_Id),
);

CREATE TABLE inventory (
inventory_Id int IDENTITY(1,1) Not Null,
store_Id int Not Null,
item_Id int Not Null,
itemInfo varchar(50) Not Null,
qtyInStock int Not Null,
PRIMARY KEY (inventory_Id),
FOREIGN KEY (store_Id) REFERENCES store(store_Id),
FOREIGN KEY (item_Id) REFERENCES item(item_Id)
)

CREATE TABLE customer (
cust_Id int IDENTITY(1,1) Not Null,
custName varchar(50) Not Null,
phone bigint Not Null,
email varchar(50) Not Null,
dateJoined date Not Null,
PRIMARY KEY (cust_Id)
);

CREATE TABLE checkout (
transaction_Id int IDENTITY(1,1) Not Null,
emp_Id int Not Null,
cust_Id int Not Null,
subtotal decimal(10,2) Not Null,
created_at datetime default current_timestamp,
PRIMARY KEY (transaction_Id),
FOREIGN KEY (emp_Id) REFERENCES cashier(emp_Id),
FOREIGN KEY (cust_Id) REFERENCES customer(cust_Id)
);

CREATE TABLE checkoutDetails (
transaction_Id int Not Null,
inventory_Id int Not Null,
quantity int Not Null,
PRIMARY KEY (transaction_Id, inventory_Id),
FOREIGN KEY (transaction_Id) REFERENCES checkout(transaction_Id),
FOREIGN KEY (inventory_Id) REFERENCES inventory(inventory_Id)
);

INSERT INTO store (address) VALUES
('123 Main St'),
('456 Elm St'),
('789 Oak St'),
('321 Pine St'),
('654 Maple St');

INSERT INTO employee (storeRef_Id,manager_Id, empName, username, password, SSN, email, phone, empAddress, payType, dateHired, dateStart, dateEnd, pay)
VALUES
  (1,2, 'John Doe', 'johndoe', 'password123', 123456789, 'johndoe@example.com', 1234567890, '123 Main St', 1, '2022-01-01', '2022-01-01', NULL, 52000.00),
  (2,3, 'Jane Smith', 'janesmith', 'password456', 987654321, 'janesmith@example.com', 9876543210, '456 Oak Ave', 1, '2022-02-01', '2022-02-01', NULL, 16000.00),
  (3,NULL, 'Michael Johnson', 'michaeljohnson', 'password789', 555555555, 'michaeljohnson@example.com', 5555555555, '789 Elm St', 1, '2022-03-01', '2022-03-01', NULL, 20000.00),
  (4,5, 'Emily Davis', 'emilydavis', 'passwordabc', 444444444, 'emilydavis@example.com', 4444444444, '987 Pine Ave', 1, '2022-04-01', '2022-04-01', NULL, 43000.00),
  (5,1, 'David Wilson', 'davidwilson', 'passworddef', 222222222, 'davidwilson@example.com', 2222222222, '654 Maple St', 1, '2022-05-01', '2022-05-01', NULL, 18000.00),
  (1,2, 'Olivia Brown', 'oliviabrown', 'passwordeg', 777777777, 'oliviabrown@example.com', 7777777777, '321 Cedar Ave', 0, '2022-06-01', '2022-06-01', NULL, 19.00),
  (2,3, 'Sophia Taylor', 'sophiataylor', 'passwordhij', 666666666, 'sophiataylor@example.com', 6666666666, '456 Birch Rd', 0, '2022-07-01', '2022-07-01', NULL, 17.50),
  (3,4, 'Matthew Anderson', 'matthewanderson', 'passwordklm', 888888888, 'matthewanderson@example.com', 8888888888, '789 Oak St',0, '2022-08-01', '2022-08-01', '2022-12-31', 16.75),
  (4,5, 'Emma Martinez', 'emmamartinez', 'passwordnop', 999999999, 'emmamartinez@example.com', 9999999999, '987 Pine Rd', 0, '2022-09-01', '2022-09-01', '2022-12-31', 15.75),
  (5,1, 'Liam Hernandez', 'liamhernandez', 'passwordqrs', 333333333, 'liamhernandez@example.com', 3333333333, '654 Elm Ave', 0, '2022-10-01', '2022-10-01', '2022-12-31', 16.25);

-- Inserting data into the manager table
INSERT INTO manager (emp_Id, director)
VALUES
(1, 1),
(2, 0),
(3, 1),
(4, 0),
(5, 0);

-- Inserting data into the cashier table
INSERT INTO cashier (emp_Id)
VALUES
  (6),
  (7),
  (8),
  (9),
  (10)

-- Inserting data into the dependent table
INSERT INTO dependent (emp_Id, name, relation)
VALUES
  (1, 'Emily Doe', 'Child'),
  (2, 'Jacob Smith', 'Spouse'),
  (3, 'Emma Johnson', 'Child'),
  (4, 'Sophia Davis', 'Child'),
  (5, 'Oliver Wilson', 'Child'),
  (6, 'Sarah Doe', 'Spouse'),
  (7, 'Emily Smith', 'Child'),
  (8, 'Jacob Johnson', 'Child'),
  (9, 'Olivia Davis', 'Child'),
  (10, 'Ethan Wilson', 'Child');

-- Inserting data into the item table
INSERT INTO item (brand, description, price, cost, shape, size, UPC, weight, taxable)
VALUES
  ('Brand A', 'Product A', 5.99, 3.50, 'Rectangle', 'Medium', 1234567890, 1.0, 1),
  ('Brand B', 'Product B', 9.99, 7.50, 'Circle', 'Large', 9876543210, 2.0, 1),
  ('Brand C', 'Product C', 3.99, 2.50, 'Square', 'Small', 5555555555, 0.5, 1),
  ('Brand D', 'Product D', 6.99, 4.50, 'Triangle', 'Medium', 2222222222, 1.5, 1),
  ('Brand E', 'Product E', 2.99, 1.50, 'Rectangle', 'Small', 9999999999, 0.75, 1),
  ('Brand F', 'Product F', 7.99, 5.50, 'Circle', 'Small', 1111111111, 0.8, 1),
  ('Brand G', 'Product G', 4.99, 3.25, 'Rectangle', 'Large', 2222222222, 1.2, 1),
  ('Brand H', 'Product H', 6.49, 4.75, 'Square', 'Medium', 3333333333, 1.5, 1),
  ('Brand I', 'Product I', 3.49, 2.25, 'Triangle', 'Small', 4444444444, 0.7, 1),
  ('Brand J', 'Product J', 1.99, 1.00, 'Circle', 'Extra Large', 5555555555, 2.5, 1);

-- Inserting data into the inventory table
INSERT INTO inventory (store_Id, item_Id, itemInfo, qtyInStock)
VALUES
  (1, 1, 'Wooden Table', 100),
  (2, 1, 'Wooden Table', 50),
  (1, 2, 'Leather Chair', 50),
  (2, 3, 'Glass Coffee Table', 200),
  (2, 4, 'Metal Chair', 75),
  (3, 5, 'Plastic Stool', 150),
  (3, 6, 'Fabric Sofa', 100),
  (4, 7, 'Marble Dining Table', 100),
  (5, 8, 'Bean Bag Chair', 80),
  (5, 9, 'Wicker Armchair', 60),
  (1, 10, 'Adjustable Standing Desk', 120);

-- Inserting data into the customer table
INSERT INTO customer (custName, phone, email, dateJoined)
VALUES
  ('Alice Johnson', 5555555555, 'alicejohnson@example.com', '2022-01-01'),
  ('Bob Smith', 6666666666, 'bobsmith@example.com', '2022-02-01'),
  ('Charlie Davis', 7777777777, 'charliedavis@example.com', '2022-03-01'),
  ('David Wilson', 8888888888, 'davidwilson@example.com', '2022-04-01'),
  ('Emma Taylor', 9999999999, 'emmataylor@example.com', '2022-05-01'),
  ('Frank Johnson', 4444444444, 'frankjohnson@example.com', '2022-06-01'),
  ('Grace Smith', 3333333333, 'gracesmith@example.com', '2022-07-01'),
  ('Henry Davis', 2222222222, 'henrydavis@example.com', '2022-08-01'),
  ('Isabella Wilson', 1111111111, 'isabellawilson@example.com', '2022-09-01'),
  ('Jack Taylor', 9999999998, 'jacktaylor@example.com', '2022-10-01');

-- Inserting data into the checkout table
INSERT INTO checkout (emp_Id, cust_Id, subtotal)
VALUES
  (6, 1, 31.96),
  (7, 2, 19.98),
  (8, 3, 15.96),
  (9, 4, 20.97),
  (10, 5, 2.99),
  (7, 2, 19.98),
  (8, 1, 15.97),
  (9, 2, 9.99),
  (10, 3, 11.98),
  (7, 4, 6.49),
  (6, 5, 13.99),
  (9, 2, 19.98);

-- Inserting data into the checkoutDetails table
INSERT INTO checkoutDetails (transaction_Id, inventory_Id, quantity)
VALUES
  (1, 1, 2),
  (1, 2, 2),
  (2, 2, 1),
  (3, 3, 4),
  (4, 4, 3),
  (5, 5, 1),
  (6, 2, 2),
  (7, 4, 1),
  (8, 5, 2),
  (9, 1, 3),
  (10, 2, 1),
  (11, 3, 2),
  (12, 8, 4)
 
