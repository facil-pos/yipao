

SQL_PROMPT = """As a {dialect_name} expert, your task is to generate SQL queries based on user questions. Ensure that your {dialect_name} queries are syntactically correct and tailored to the user's inquiry. Retrieve at most 10 results using and order them for relevance. Avoid querying for all columns from a table. Select only the necessary columns wrapped in backticks (`).  Stop after delivering the SQLQuery, avoiding follow-up questions.

only use the following tables, the ddl of each table will be shown: 
{table_names}

Exemple of questions and SQL QUERY:

What is my best-selling product in the month of August? -> "SELECT si.item_id, si.name_combined AS product_name, SUM(si.quantity_purchased) AS total_quantity
FROM phppos_sales s
JOIN phppos_sales_items si ON s.sale_id = si.sale_id
WHERE s.sale_time BETWEEN '2023-08-01 00:00:00' AND '2023-08-31 23:59:59'
AND s.tipo IN ('sale', 'ND')
AND s.deleted = 0
GROUP BY si.item_id, si.name_combined
ORDER BY total_quantity DESC
LIMIT 1;"
"What are my five best-selling products during the month of July?" -> "SELECT si.item_id, si.name_combined AS product_name, SUM(si.quantity_purchased) AS total_quantity
FROM phppos_sales s
JOIN phppos_sales_items si ON s.sale_id = si.sale_id
WHERE s.sale_time BETWEEN '2023-07-01 00:00:00' AND '2023-07-31 23:59:59'
AND s.tipo IN ('sale', 'ND')
AND s.deleted = 0
GROUP BY si.item_id, si.name_combined
ORDER BY total_quantity DESC
LIMIT 5;"
Who are my five best clients for the month of April? -> "# Reports TOP 5 clientes
select
        s.name_customer_c  as 'Client',
    FORMAT(SUM(s.subtotal), 0) AS 'Totla'
FROM
    phppos_sales AS s
GROUP BY s.customer_id
ORDER BY
    s.subtotal DESC
LIMIT 5;"
Who was the customer who made the most purchases in June? -> "SELECT COUNT(*)
FROM phppos_sales s
WHERE YEAR(s.sale_time) = 2023
  AND MONTH(s.sale_time) = 5;

SELECT CONCAT(p.first_name,' ',p.last_name) as name_customer, COUNT(s.customer_id) AS quantity_sales
FROM phppos_sales s
JOIN phppos_customers c ON s.customer_id = c.person_id 
JOIN phppos_people p ON s.customer_id = p.person_id
WHERE s.sale_time BETWEEN '2024-01-01 00:00:00' AND '2024-06-30 23:59:59'
AND s.tipo IN ('sale', 'ND')
AND s.deleted = 0
AND c.deleted = 0
GROUP BY s.customer_id
ORDER BY quantity_sales DESC
LIMIT 5;"
How many customers made purchases in August? -> "SELECT COUNT(DISTINCT s.customer_id) AS total_customers
FROM phppos_sales s
JOIN phppos_customers c ON s.customer_id = c.person_id 
WHERE s.sale_time BETWEEN '2024-01-01 00:00:00' AND '2024-06-30 23:59:59'
AND s.tipo IN ('sale', 'ND')
AND s.deleted = 0
AND c.deleted = 0;"
Which clients have increased or decreased their spending in the last three months?	"SELECT 
    CONCAT(p.first_name,' ',p.last_name) AS name_customer,
    SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND NOW() THEN 1 ELSE 0 END) AS quantity_sales_current,
    SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND DATE_SUB(NOW(), INTERVAL 3 MONTH) THEN 1 ELSE 0 END) AS quantity_sales_previous,
    CASE 
        WHEN SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND NOW() THEN 1 ELSE 0 END) > SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND DATE_SUB(NOW(), INTERVAL 3 MONTH) THEN 1 ELSE 0 END) THEN 'Aumentó'
        WHEN SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND NOW() THEN 1 ELSE 0 END) < SUM(CASE WHEN s.sale_time BETWEEN DATE_SUB(NOW(), INTERVAL 6 MONTH) AND DATE_SUB(NOW(), INTERVAL 3 MONTH) THEN 1 ELSE 0 END) THEN 'Disminuyó'
        ELSE 'Igual'
    END AS status
FROM 
    phppos_sales s
JOIN 
    phppos_customers c ON s.customer_id = c.person_id 
JOIN 
    phppos_people p ON s.customer_id = p.person_id
WHERE 
    s.tipo IN ('sale', 'ND')
    AND s.deleted = 0
    AND c.deleted = 0
GROUP BY 
    s.customer_id
ORDER BY 
    quantity_sales_current DESC;" 
How many new customers bought in the month of June? -> "SELECT 
    CONCAT(p.first_name,' ',p.last_name) AS name_customer, 
    COUNT(s.customer_id) AS quantity_sales
FROM 
    phppos_sales s
JOIN 
    phppos_customers c ON s.customer_id = c.person_id 
JOIN 
    phppos_people p ON s.customer_id = p.person_id
WHERE 
    s.sale_time BETWEEN '2024-05-01 00:00:00' AND '2024-05-30 23:59:59'
    AND s.tipo IN ('sale', 'ND')
    AND s.deleted = 0
    AND c.deleted = 0
    AND s.customer_id NOT IN (
        SELECT s2.customer_id
        FROM phppos_sales s2
        JOIN phppos_customers c2 ON s2.customer_id = c.person_id 
        WHERE s2.sale_time < '2024-05-01 00:00:00'
        AND s2.tipo IN ('sale', 'ND')
		AND s2.deleted = 0
		AND c2.deleted = 0
    )
GROUP BY 
    s.customer_id
ORDER BY 
    quantity_sales DESC;"
Which customer stopped buying in July after being a regular buyer? -> "-- Para resolver este Query se debe definir que es un comprador habitual.
-- Para el ejemplo se tomo como comprador habitual aquel que realiza almenos una compra al mes durante 3 meses de seguido.
SET @base_month = '2023-09-01';

SELECT s.customer_id AS id_customer, 
       CONCAT(p.first_name, ' ', p.last_name) AS name_customer,
       COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 3 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) AS compras_hace_3_meses,
       COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 2 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) AS compras_hace_2_meses,
       COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 1 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) AS compras_hace_1_mes,
       COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(@base_month, '%Y-%m') THEN s.customer_id ELSE NULL END) AS compras_este_mes,
       CASE 
           WHEN COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(@base_month, '%Y-%m') THEN s.customer_id ELSE NULL END) = 0 AND 
                COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 1 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) > 0 AND 
                COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 2 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) > 0 AND
                COUNT(CASE WHEN DATE_FORMAT(s.sale_time, '%Y-%m') = DATE_FORMAT(DATE_SUB(@base_month, INTERVAL 3 MONTH), '%Y-%m') THEN s.customer_id ELSE NULL END) > 0
           THEN 'dejo de comprar'
           ELSE 'No es comprador habitual'
       END AS estado_cliente
FROM phppos_sales s
JOIN phppos_customers c ON s.customer_id = c.person_id 
JOIN phppos_people p ON s.customer_id = p.person_id
WHERE s.sale_time BETWEEN DATE_SUB(@base_month, INTERVAL 3 MONTH) AND LAST_DAY(@base_month)
  AND s.tipo IN ('sale', 'ND')
  AND s.deleted = 0
  AND c.deleted = 0
GROUP BY s.customer_id, p.first_name, p.last_name
HAVING compras_hace_3_meses > 0 OR compras_hace_2_meses > 0 OR compras_hace_1_mes > 0 OR compras_este_mes > 0;"
How many customers did not make purchases in May but did make purchases in June? -> "# Clientes que no realizaron compras en mayo
SELECT DISTINCT customer_id
FROM phppos_sales
WHERE sale_time NOT BETWEEN '2023-05-01 00:00:00' AND '2023-05-31 23:59:59';


# Clientes que sí realizaron compras en junio
SELECT DISTINCT customer_id
FROM phppos_sales
WHERE sale_time BETWEEN '2023-06-01 00:00:00' AND '2023-06-30 23:59:59';


# Clientes que no compraron en mayo, pero sí en junio
SELECT COUNT(*)
FROM (
    SELECT DISTINCT june_customers.customer_id
    FROM (
        SELECT DISTINCT customer_id
        FROM phppos_sales
        WHERE sale_time BETWEEN '2023-06-01 00:00:00' AND '2023-06-30 23:59:59'
    ) AS june_customers
    LEFT JOIN (
        SELECT DISTINCT customer_id
        FROM phppos_sales
        WHERE sale_time BETWEEN '2023-05-01 00:00:00' AND '2023-05-31 23:59:59'
    ) AS may_customers
    ON june_customers.customer_id = may_customers.customer_id
    WHERE may_customers.customer_id IS NULL
) AS result;"
What was the total revenue generated by returning customers in July? -> "# Ingresos por cliente
SELECT
    s.name_customer_c AS 'Client',
    FORMAT(SUM(
        (si.item_unit_price * si.quantity_purchased - si.item_unit_price * si.quantity_purchased * si.discount_percent / 100) -
        (si.item_cost_price * si.quantity_purchased)
    ), 0) AS 'Ganancia Item'
FROM
    phppos_sales AS s
    INNER JOIN phppos_sales_items AS si ON si.sale_id = s.sale_id
WHERE
    s.sale_time BETWEEN '2023-01-01 00:00:00' AND '2023-12-31 23:59:59'
GROUP BY
    s.customer_id
ORDER BY
    SUM(
        (si.item_unit_price * si.quantity_purchased - si.item_unit_price * si.quantity_purchased * si.discount_percent / 100) -
        (si.item_cost_price * si.quantity_purchased)
    ) DESC;
"
Who was my best-selling seller in August? -> "# Empleado  con mayor numero de ventas
SELECT
    pe.username as 'Empleado',
    SUM(s.subtotal) as 'Total vendio'
FROM
    phppos_sales AS s
    INNER JOIN phppos_employees pe ON pe.id = s.employee_id 
WHERE
    s.sale_time BETWEEN '2023-08-01 00:00:00' AND '2023-09-01 23:59:59'
GROUP BY
    s.employee_id 
ORDER BY
    count(*)  desc
limit 1;"
Which sellers generated the least sales in the month of June? -> "# Empleado  con menor numero de ventas
SELECT
    pe.username as 'Empleado',
    SUM(s.subtotal) as 'Total vendio'
FROM
    phppos_sales AS s
    INNER JOIN phppos_employees pe ON pe.id = s.employee_id 
WHERE
    s.sale_time BETWEEN '2023-08-01 00:00:00' AND '2023-09-01 23:59:59'
GROUP BY
    s.employee_id 
ORDER BY
    count(*)  asc limit 1;"

Question from the user:
"{question}"

History:
{history}

Use the history as a guide.
Be careful with the names of the tables and columns, if necessary make the respective joins.
Be careful with the names of the columns and their respective tables to avoid consulting non-existent columns.
You must use the tables provided. 

Do not include explanatory text. Only generate the final SQL query wrapped in the JSON format below:
{{
    "sql_query": "your sql query here"
}}

"""



FINAL_RESPONSE_PROMPT = """You are the helpful assistant designed to answer user questions based on the data provided from the database in context. Your goal is to analyze the user's query and provide a helpful response using only the information available in the context. If Context is None or Empty, say you don't have the data to answer the question.

DATAFRAME CONTEXT:
{context_df}

USER QUESTION:
{user_query}

ASSISTANT RESPONSE:
"""

