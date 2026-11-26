-- Todas las filas de los tres resultados deben mostrar correcto = true.

-- Filas esperadas en cada tabla al cerrar el Lab 2.
WITH conteos (tabla, filas_esperadas, filas_observadas) AS (
    SELECT 'customers', 2, COUNT(*) FROM public.customers
    UNION ALL SELECT 'products', 6, COUNT(*) FROM public.products
    UNION ALL SELECT 'orders', 4, COUNT(*) FROM public.orders
    UNION ALL SELECT 'order_items', 8, COUNT(*) FROM public.order_items
    UNION ALL SELECT 'inventory', 6, COUNT(*) FROM public.inventory
)
SELECT tabla, filas_esperadas, filas_observadas,
       filas_observadas = filas_esperadas AS correcto
FROM conteos
ORDER BY tabla;

-- Totales históricos. Un pedido ausente se muestra como incorrecto.
WITH totales AS (
    SELECT order_id, SUM(quantity * unit_price) AS total_eur
    FROM public.order_items
    GROUP BY order_id
)
SELECT e.order_id, e.total_esperado_eur, t.total_eur AS total_observado_eur,
       COALESCE(t.total_eur = e.total_esperado_eur, FALSE) AS correcto
FROM (VALUES (1001, 17.00), (1002, 11.00), (1003, 9.00), (1004, 6.50))
    AS e (order_id, total_esperado_eur)
LEFT JOIN totales AS t ON t.order_id = e.order_id
ORDER BY e.order_id;

-- Stock reservado para el ejercicio del Lab 3. Una fila ausente da false.
SELECT e.product_id, e.stock_esperado, i.stock AS stock_observado,
       COALESCE(i.stock = e.stock_esperado, FALSE) AS correcto
FROM (VALUES (4, 1)) AS e (product_id, stock_esperado)
LEFT JOIN public.inventory AS i ON i.product_id = e.product_id;
