-- C2. Ejecuta este bloque mientras A conserva el bloqueo. B lee stock 1.
SET application_name = 'terra-lab3-B';
BEGIN ISOLATION LEVEL READ COMMITTED;

SELECT stock FROM public.inventory WHERE product_id = 4;

SELECT price FROM public.products WHERE product_id = 4;

INSERT INTO public.orders (order_id, customer_id, order_date)
VALUES (2003, 2, CURRENT_DATE);

INSERT INTO public.order_items (order_id, product_id, quantity, unit_price)
SELECT 2003, product_id, 1, price
FROM public.products
WHERE product_id = 4;

-- Descuento de B14 para una unidad. El CHECK rechaza el stock negativo.
UPDATE public.inventory
SET stock = stock - 1
WHERE product_id = 4
RETURNING product_id, stock;

-- PAUSA. El UPDATE espera. Sigue con C3 y C4 en A.

-- C5. Después del COMMIT de A, el UPDATE de B falla por el CHECK (23514).
ROLLBACK;

SELECT COUNT(*) AS pedidos_2003 FROM public.orders WHERE order_id = 2003;
SELECT COUNT(*) AS lineas_2003 FROM public.order_items WHERE order_id = 2003;
