-- C1. Ejecuta hasta el UPDATE y deja abierta la transacción.
SET application_name = 'terra-lab3-A';
BEGIN ISOLATION LEVEL READ COMMITTED;

SELECT stock FROM public.inventory WHERE product_id = 4;

SELECT price FROM public.products WHERE product_id = 4;

INSERT INTO public.orders (order_id, customer_id, order_date)
VALUES (2002, 1, CURRENT_DATE);

INSERT INTO public.order_items (order_id, product_id, quantity, unit_price)
SELECT 2002, product_id, 1, price
FROM public.products
WHERE product_id = 4;

UPDATE public.inventory
SET stock = stock - 1
WHERE product_id = 4 AND stock >= 1
RETURNING product_id, stock;

-- PAUSA. Ejecuta C2 en B mientras A conserva el bloqueo.

-- C3. Con B esperando, identifica su bloqueo desde A.
SELECT pid, wait_event_type, wait_event, pg_blocking_pids(pid) AS bloqueadores
FROM pg_stat_activity
WHERE datname = current_database() AND application_name = 'terra-lab3-B';

-- C4. Si C1 devolvió UPDATE 1, confirma el pedido y libera el bloqueo.
COMMIT;

SELECT COUNT(*) AS pedidos_2002 FROM public.orders WHERE order_id = 2002;
SELECT COUNT(*) AS lineas_2002 FROM public.order_items WHERE order_id = 2002;
