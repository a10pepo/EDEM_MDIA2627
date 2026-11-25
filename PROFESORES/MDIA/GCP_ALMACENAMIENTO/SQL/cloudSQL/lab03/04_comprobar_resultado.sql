-- Tras los tres experimentos, los stocks de los productos 1 y 4 son 22 y 0.
SELECT product_id, stock
FROM public.inventory
WHERE product_id IN (1, 4)
ORDER BY product_id;

-- Quedan las compras de María (2002, caja) y Juan (2004, naranja).
SELECT o.order_id, c.name AS cliente, oi.product_id, oi.quantity, oi.unit_price
FROM public.orders AS o
JOIN public.customers AS c ON c.customer_id = o.customer_id
LEFT JOIN public.order_items AS oi ON oi.order_id = o.order_id
WHERE o.order_id IN (2001, 2002, 2003, 2004)
ORDER BY o.order_id, oi.product_id;

-- Debe haberse vendido una única unidad del producto 4.
SELECT COUNT(*) AS lineas_de_venta, COALESCE(SUM(quantity), 0) AS unidades_vendidas
FROM public.order_items
WHERE product_id = 4;
