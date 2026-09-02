USE cynaris_sales;

SELECT *
FROM sales;
SELECT customer_name, product, price
FROM sales;
SELECT *
FROM sales
WHERE price > 1000;
SELECT *
FROM sales
WHERE category = 'Electronics'
AND price > 5000;
SELECT *
FROM sales
WHERE city = 'Bangalore'
OR city = 'Chennai';
SELECT *
FROM sales
WHERE NOT category = 'Clothing';
SELECT *
FROM sales
WHERE customer_name LIKE 'A%';
SELECT *
FROM sales
WHERE city IN ('Bangalore', 'Chennai', 'Mumbai');
SELECT *
FROM sales
WHERE price BETWEEN 1000 AND 5000;
SELECT *
FROM sales
WHERE discount IS NULL;