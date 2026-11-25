-- COMPRA CONFIRMADA. Ejecuta un paso cada vez.

-- B1. Abre la transacción.
BEGIN;

-- B2. Quedan 23 naranjas tras el experimento A.
SELECT stock FROM public.inventory WHERE product_id = 1;

-- B3. La naranja cuesta 2.50 por unidad.
SELECT price FROM public.products WHERE product_id = 1;

-- B4. Registra el pedido de Juan.
INSERT INTO public.orders (order_id, customer_id, order_date)
VALUES (2004, 2, CURRENT_DATE);

-- B5. Registra una naranja al precio del catálogo.
INSERT INTO public.order_items (order_id, product_id, quantity, unit_price)
SELECT 2004, product_id, 1, price
FROM public.products
WHERE product_id = 1;

-- B6. Descuenta una unidad. Espera UPDATE 1 y stock 22.
UPDATE public.inventory
SET stock = stock - 1
WHERE product_id = 1 AND stock >= 1
RETURNING product_id, stock;

-- B7. Confirma si B6 devolvió UPDATE 1.
COMMIT;

-- B8. Comprueba el pedido, la línea y el stock confirmado.
SELECT order_id, customer_id FROM public.orders WHERE order_id = 2004;
SELECT product_id, quantity, unit_price FROM public.order_items WHERE order_id = 2004;
SELECT stock FROM public.inventory WHERE product_id = 1;

-- COMPRA FALLIDA. Ejecuta un paso cada vez.

-- B9. Abre la transacción.
BEGIN;

-- B10. Queda una caja. Continúa para provocar el error del ejercicio.
SELECT stock FROM public.inventory WHERE product_id = 4;

-- B11. La caja cuesta 12.00 por unidad.
SELECT price FROM public.products WHERE product_id = 4;

-- B12. Registra el pedido de María.
INSERT INTO public.orders (order_id, customer_id, order_date)
VALUES (2001, 1, CURRENT_DATE);

-- B13. Registra dos cajas al precio unitario del catálogo.
INSERT INTO public.order_items (order_id, product_id, quantity, unit_price)
SELECT 2001, product_id, 2, price
FROM public.products
WHERE product_id = 4;

-- B14. Intenta restar dos unidades. El CHECK rechaza el stock de -1.
UPDATE public.inventory
SET stock = stock - 2
WHERE product_id = 4;

-- B15. Revierte el pedido y la línea tras el error.
ROLLBACK;

-- B16. Confirma que queda una caja y que el pedido y su línea desaparecieron.
SELECT COUNT(*) AS pedidos_2001 FROM public.orders WHERE order_id = 2001;
SELECT COUNT(*) AS lineas_2001 FROM public.order_items WHERE order_id = 2001;
SELECT stock FROM public.inventory WHERE product_id = 4;
