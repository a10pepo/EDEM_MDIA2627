-- La base debe ser terra_taronja. Los dos psql deben mostrar PID distintos.
SELECT current_database() AS base, pg_backend_pid() AS pid;

SELECT e.product_id, e.stock AS esperado, i.stock AS observado,
       COALESCE(i.stock = e.stock, FALSE) AS correcto
FROM (VALUES (1, 24), (4, 1)) AS e (product_id, stock)
LEFT JOIN public.inventory AS i ON i.product_id = e.product_id
ORDER BY e.product_id;

-- Las dos comprobaciones deben dar true.
SELECT NOT EXISTS (
           SELECT 1 FROM public.orders WHERE order_id IN (2001, 2002, 2003, 2004)
       ) AS ids_libres,
       NOT EXISTS (
           SELECT 1 FROM public.order_items WHERE product_id = 4
       ) AS caja_sin_ventas;
