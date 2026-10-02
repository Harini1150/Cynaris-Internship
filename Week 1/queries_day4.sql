USE cynaris_sales;

-- 1. Non-correlated subquery - Sales above average
SELECT
    sale_id,
    customer_name,
    product,
    quantity * price AS sale_amount
FROM sales
WHERE quantity * price > (
    SELECT AVG(quantity * price)
    FROM sales
);
SELECT AVG(quantity * price)
FROM sales
-- 2. Correlated subquery - Top sale per city
SELECT
    s1.sale_id,
    s1.customer_name,
    s1.product,
    s1.city,
    s1.quantity * s1.price AS sale_amount
FROM sales s1
WHERE s1.quantity * s1.price = (
    SELECT MAX(s2.quantity * s2.price)
    FROM sales s2
    WHERE s2.city = s1.city
);
-- 3. CTE - Category-wise sales above average
WITH category_sales AS (
    SELECT
        category,
        SUM(quantity * price) AS total_sales
    FROM sales
    GROUP BY category
)
SELECT
    category,
    total_sales
FROM category_sales
WHERE total_sales > (
    SELECT AVG(total_sales)
    FROM category_sales
);
WITH category_sales AS (...)
-- 3. CTE - Category-wise sales above average
WITH category_sales AS (
    SELECT
        category,
        SUM(quantity * price) AS total_sales
    FROM sales
    GROUP BY category
)
SELECT
    category,
    total_sales
FROM category_sales
WHERE total_sales > (
    SELECT AVG(total_sales)
    FROM category_sales
);
-- 4. Chaining two CTEs - Category sales and average sales
WITH category_sales AS (
    SELECT
        category,
        SUM(quantity * price) AS total_sales
    FROM sales
    GROUP BY category
),
average_sales AS (
    SELECT
        AVG(total_sales) AS avg_category_sales
    FROM category_sales
)
SELECT
    cs.category,
    cs.total_sales,
    a.avg_category_sales
FROM category_sales cs
CROSS JOIN average_sales a
WHERE cs.total_sales > a.avg_category_sales;