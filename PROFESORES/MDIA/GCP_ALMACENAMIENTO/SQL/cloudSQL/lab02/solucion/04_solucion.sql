-- 1. Productos por encima de 4 euros.
SELECT product_id, name, price
FROM public.products
WHERE price > 4.00
ORDER BY price, product_id;

-- 2. Compras de Juan en los pedidos 1002 y 1004.
SELECT c.name AS cliente, o.order_id, p.name AS producto,
       oi.quantity, oi.unit_price AS precio_historico
FROM public.customers AS c
JOIN public.orders AS o ON o.customer_id = c.customer_id
JOIN public.order_items AS oi ON oi.order_id = o.order_id
JOIN public.products AS p ON p.product_id = oi.product_id
WHERE c.customer_id = 2
ORDER BY o.order_id, p.product_id;

-- 3. Gasto por cliente. María 26.00 y Juan 17.50.
SELECT c.customer_id, c.name AS cliente,
       SUM(oi.quantity * oi.unit_price) AS total_eur
FROM public.customers AS c
JOIN public.orders AS o ON o.customer_id = c.customer_id
JOIN public.order_items AS oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

-- 4. Queda una unidad de la caja de naranjas de temporada.
SELECT p.name AS producto, i.stock
FROM public.inventory AS i
JOIN public.products AS p ON p.product_id = i.product_id
WHERE i.stock < 5
ORDER BY i.stock, p.product_id;

-- 5. En el pedido 1001 se cobraron 11.00 por la naranja y 6.00 por el zumo.
SELECT p.name AS producto, oi.quantity * oi.unit_price AS importe_eur
FROM public.order_items AS oi
JOIN public.products AS p ON p.product_id = oi.product_id
WHERE oi.order_id = 1001
ORDER BY p.product_id;

-- 6. Unidades vendidas por producto, incluidos los que aún no tienen ventas.
SELECT p.name AS producto, COALESCE(SUM(oi.quantity), 0) AS unidades_vendidas
FROM public.products AS p
LEFT JOIN public.order_items AS oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY p.product_id;

-- 7. El pedido más caro es el 1001 de María, por 17.00.
SELECT o.order_id, c.name AS cliente, SUM(oi.quantity * oi.unit_price) AS total_eur
FROM public.orders AS o
JOIN public.customers AS c ON c.customer_id = o.customer_id
JOIN public.order_items AS oi ON oi.order_id = o.order_id
GROUP BY o.order_id, c.name
ORDER BY total_eur DESC, o.order_id
LIMIT 1;

-- 8. Ejecuta desde BEGIN hasta ROLLBACK en una sola ejecución.
-- Los pedidos 1001 y 1002 muestran 3.50 en catálogo y 3.00 en su línea.
BEGIN;

UPDATE public.products
SET price = 3.50
WHERE product_id = 2;

SELECT oi.order_id, p.name AS producto,
       p.price AS precio_catalogo, oi.unit_price AS precio_historico
FROM public.order_items AS oi
JOIN public.products AS p ON p.product_id = oi.product_id
WHERE p.product_id = 2
ORDER BY oi.order_id;

ROLLBACK;
