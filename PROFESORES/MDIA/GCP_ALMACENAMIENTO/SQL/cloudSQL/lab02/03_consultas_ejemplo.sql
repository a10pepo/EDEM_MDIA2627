-- 1. SELECT. Muestra los precios actuales de los seis productos.
SELECT product_id, name, price
FROM public.products
ORDER BY product_id;

-- 2. JOIN. Identifica al cliente de cada pedido.
SELECT o.order_id, c.name AS cliente, o.order_date
FROM public.orders AS o
JOIN public.customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id;

-- 3. GROUP BY y SUM. Agrupa las líneas por pedido y suma sus importes históricos.
SELECT order_id, SUM(quantity * unit_price) AS total_eur
FROM public.order_items
GROUP BY order_id
ORDER BY order_id;

-- 4. UPDATE. Ejecuta el bloque completo, desde BEGIN hasta ROLLBACK.
-- El catálogo muestra 6.00. Las líneas de los pedidos 1001 y 1004 conservan
-- 5.50 y 2.50, respectivamente.
BEGIN;

UPDATE public.products
SET price = 6.00
WHERE product_id = 1;

SELECT oi.order_id, p.name AS producto,
       p.price AS precio_catalogo, oi.unit_price AS precio_historico
FROM public.order_items AS oi
JOIN public.products AS p ON p.product_id = oi.product_id
WHERE p.product_id = 1
ORDER BY oi.order_id;

ROLLBACK;
