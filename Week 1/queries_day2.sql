USE cynaris_sales;

INSERT INTO customers
(customer_id, customer_name, city)
VALUES
(1, 'Arun', 'Bangalore'),
(2, 'Priya', 'Chennai'),
(3, 'Rahul', 'Mumbai'),
(4, 'Ananya', 'Bangalore'),
(5, 'Kiran', 'Hyderabad'),
(6, 'Asha', 'Chennai'),
(7, 'Amit', 'Mumbai'),
(8, 'Sneha', 'Bangalore'),
(9, 'Vikram', 'Delhi'),
(10, 'Divya', 'Hyderabad'),
(11, 'Meena', 'Pune');
SELECT * FROM customers;
SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
INNER JOIN sales
ON customers.customer_name = sales.customer_name;
-- 2. LEFT JOIN
SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
LEFT JOIN sales
ON customers.customer_name = sales.customer_name;
-- 3. RIGHT JOIN
SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
RIGHT JOIN sales
ON customers.customer_name = sales.customer_name;
-- 4. FULL OUTER JOIN
SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
LEFT JOIN sales
ON customers.customer_name = sales.customer_name

UNION

SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
RIGHT JOIN sales
ON customers.customer_name = sales.customer_name;
-- 5. Duplicate rows example
SELECT
    customers.customer_name,
    customers.city,
    sales.product
FROM customers
JOIN sales
ON customers.city = sales.city;
-- 6. Fix duplicate rows using a unique matching column
SELECT
    customers.customer_name,
    customers.city,
    sales.product,
    sales.price
FROM customers
JOIN sales
ON customers.customer_name = sales.customer_name;
-- 7. Create employees table for self-join

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT
);
INSERT INTO employees
(employee_id, employee_name, manager_id)
VALUES
(1, 'Ravi', NULL),
(2, 'Priya', 1),
(3, 'Arun', 1),
(4, 'Sneha', 2),
(5, 'Kiran', 2);
-- 7. SELF JOIN
SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.employee_id;