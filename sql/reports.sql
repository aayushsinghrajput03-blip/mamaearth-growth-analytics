-- Mamaearth Growth Analytics - Reports

-- (a) Total orders, total revenue and average order value
-- Expected output: total_orders = 180, total_revenue = 99860.20,
-- avg_order_value = 554.78
SELECT
    COUNT(*) AS total_orders,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_revenue,
    ROUND(
        AVG(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS avg_order_value
FROM orders o
JOIN products p
    ON o.product_id = p.product_id;


-- (b) Total orders vs rated orders
-- Expected output: total_orders = 180, total_rated_orders = 165,
-- difference = 15
SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS total_rated_orders,
    COUNT(*) - COUNT(rating) AS difference
FROM orders;


-- (c) Customers with zero orders
-- Expected output: C045, Vihaan
SELECT
    c.name,
    c.customer_id
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = 0;


-- Alternative zero-order customer check
-- Expected output: C045, Vihaan
SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
);


-- (d) Cities with return rate above 20%
-- Expected output:
-- Jaipur     | 19 | 8  | 42.1%
-- Lucknow    | 49 | 15 | 30.6%
-- Bangalore  | 33 | 8  | 24.2%
SELECT
    c.city,
    COUNT(*) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(
        SUM(o.returned) * 100.0 / COUNT(*),
        1
    ) AS return_rate_pct
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;


-- (e) Top 5 customers by total spend
-- Expected output:
-- C043 | Reyansh | 12920.00
-- C026 | Isha    | 8371.60
-- C008 | Meera   | 4564.60
-- C011 | Arjun   | 4111.00
-- C042 | Sanya   | 3785.00
-- Tie-breaker: customer_id ASC when total_spend is equal.
SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_spend
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;


-- Customers ranked 3rd to 5th by total spend
-- Expected output:
-- C008 | Meera | 4564.60
-- C011 | Arjun | 4111.00
-- C042 | Sanya | 3785.00
SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_spend
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;


-- (f) Category-wise order count and revenue
-- Expected output:
-- Haircare     | 54 | 44956.10
-- Skincare     | 60 | 27346.00
-- Babycare     | 30 | 16805.00
-- PersonalCare | 36 | 10753.10
SELECT
    p.category,
    COUNT(*) AS order_count,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS category_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;


-- (g) Customers whose names start with A
-- Expected output: 10 rows
SELECT
    name
FROM customers
WHERE name LIKE 'A%';


-- (h) Distinct acquisition sources
-- Expected output: Ad, Organic, Referral, Social (4 rows)
SELECT DISTINCT
    acquisition_source
FROM customers;


-- (i) Add loyalty tier based on city tier
-- Expected output after UPDATE: Gold = 28, Silver = 17
ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier = CASE
    WHEN city_tier = 1 THEN 'Gold'
    ELSE 'Silver'
END;

-- Verify loyalty tiers
SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier;
