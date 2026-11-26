BEGIN;

DO $preparar$
BEGIN
    IF current_database() <> 'terra_taronja' THEN
        RAISE EXCEPTION 'Ejecuta esta práctica en la base terra_taronja.';
    END IF;

    LOCK TABLE public.orders IN ACCESS EXCLUSIVE MODE;

    IF EXISTS (
        SELECT 1 FROM public.orders WHERE order_id BETWEEN 1000000 AND 1049999
    ) THEN
        RAISE EXCEPTION 'El rango de IDs de la práctica ya está ocupado. Revisa el estado antes de repetir.';
    END IF;

    IF (SELECT COUNT(*) FROM public.customers WHERE customer_id IN (1, 2)) <> 2 THEN
        RAISE EXCEPTION 'Faltan los clientes 1 y 2 del Lab 2.';
    END IF;

    IF to_regclass('public.idx_orders_created_at') IS NOT NULL THEN
        RAISE EXCEPTION 'Ya existe un objeto llamado idx_orders_created_at.';
    END IF;
END;
$preparar$;

-- Los pedidos existentes conservan su order_date y quedan con created_at NULL.
ALTER TABLE public.orders ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE;
COMMENT ON COLUMN public.orders.created_at IS 'Terra Taronja Lab 4 datos sintéticos';

-- Cada bloque de 365 pedidos recorre el año. El siguiente bloque avanza 10 min.
WITH sinteticos AS (
    SELECT 1000000 + n AS order_id,
           1 + n % 2 AS customer_id,
           TIMESTAMP '2026-01-01' + (n % 365) * INTERVAL '1 day'
               + (n / 365) * INTERVAL '10 minutes' AS created_at
    FROM generate_series(0, 49999) AS serie(n)
), insertados AS (
    INSERT INTO public.orders (order_id, customer_id, order_date, created_at)
    SELECT order_id, customer_id, created_at::date, created_at
    FROM sinteticos
    RETURNING created_at
)
SELECT COUNT(*) AS pedidos_sinteticos,
       COUNT(*) FILTER (
           WHERE created_at >= TIMESTAMP '2026-04-01' AND created_at < TIMESTAMP '2026-04-02'
       ) AS pedidos_del_1_de_abril
FROM insertados;

ANALYZE public.orders;

COMMIT;
