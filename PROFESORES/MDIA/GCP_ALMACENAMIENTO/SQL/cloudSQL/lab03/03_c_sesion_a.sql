SET application_name = 'terra-lab3-A';

-- C1. María intenta comprar una caja del producto 4. Empieza la transacción.
BEGIN ISOLATION LEVEL READ COMMITTED;

-- Reutiliza B2 a B6 de la compra confirmada del archivo 02.

-- B2. Consulta el stock del producto 4 en inventory con un SELECT normal.

-- B3. Consulta el precio actual del producto 4 en products.

-- B4. Registra el pedido 2002 de María (customer_id = 1), con fecha de hoy.

-- B5. Añade al pedido una línea de una caja al precio que consultaste.

-- B6. Descuenta una caja solo si queda stock. Muestra el stock resultante.


-- PAUSA. Si actualizaste una fila, deja la compra sin confirmar. Cambia a B
-- para que Juan intente comprar la misma caja. Si falla tu descuento,
-- revierte la transacción y revisa el stock inicial antes de seguir.


-- C3. Mientras B espera, vuelve a A. Busca la sesión terra-lab3-B en
-- pg_stat_activity y usa pg_blocking_pids para identificar quién la bloquea.
SELECT pid, wait_event_type, wait_event, pg_blocking_pids(pid) AS bloqueadores
FROM pg_stat_activity
WHERE datname = current_database() AND application_name = 'terra-lab3-B';

-- Confirma la compra
COMMIT;

SELECT COUNT(*) AS pedidos_2003 FROM public.orders WHERE order_id = 2002;
SELECT COUNT(*) AS lineas_2003 FROM public.order_items WHERE order_id = 2002;