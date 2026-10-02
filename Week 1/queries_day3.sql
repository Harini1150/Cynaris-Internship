USE cynaris_sales;

-- 1. COUNT - Total number of sales
SELECT COUNT(*) AS total_sales
FROM sales;
-- 2. SUM - Total sales value
SELECT SUM(quantity * price) AS total_sales_value
FROM sales;
-- 3. AVG - Average product price
SELECT AVG(price) AS average_price
FROM sales;
-- 4. MAX - Highest product price
SELECT MAX(price) AS highest_price
FROM sales;
-- 5. MIN - Lowest product price
SELECT MIN(price) AS lowest_price
FROM sales;
-- 6. GROUP BY - Sales by category
SELECT
    category,
    COUNT(*) AS number_of_sales,
    SUM(quantity * price) AS total_sales
FROM sales
GROUP BY category;
-- 7. GROUP BY - Sales by city
SELECT
    city,
    COUNT(*) AS number_of_sales,
    SUM(quantity * price) AS total_sales
FROM sales
GROUP BY city;
-- 8. GROUP BY - Sales by month
SELECT
    MONTH(sale_date) AS sale_month,
    COUNT(*) AS number_of_sales,
    SUM(quantity * price) AS total_sales
FROM sales
GROUP BY MONTH(sale_date);
-- 9. HAVING - Filter grouped results
SELECT
    category,
    COUNT(*) AS number_of_sales,
    SUM(quantity * price) AS total_sales
FROM sales
GROUP BY category
HAVING SUM(quantity * price) > 5000;
-- 10. WINDOW FUNCTION - Running total of sales
SELECT
    sale_id,
    customer_name,
    product,
    quantity * price AS sale_amount,
    SUM(quantity * price) OVER (ORDER BY sale_date) AS running_total
FROM sales;