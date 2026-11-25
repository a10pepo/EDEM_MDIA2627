-- Ejecuta este mismo archivo antes y después de crear el índice.
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id, customer_id, created_at
FROM public.orders
WHERE created_at >= TIMESTAMP '2026-04-01'
  AND created_at < TIMESTAMP '2026-04-02';
