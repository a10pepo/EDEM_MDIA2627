-- Trabaja en la pestaña A. Completa y ejecuta un paso cada vez.
-- Mira el resultado antes de seguir. Ejecuta las sentencias ya escritas en su paso.

-- COMPRA CONFIRMADA. Juan compra una naranja en el pedido 2004.

-- B1. Abre la transacción.
BEGIN;

-- B2. Escribe un SELECT en inventory para consultar el stock del producto 1. checa si hay stock disponible


-- B3. Escribe un SELECT en products para ver el precio actual del producto 1.
-- Anota el precio. Lo necesitarás en su línea de pedido.


-- B4. Inserta el pedido 2004 en orders para Juan (customer_id = 2), con fecha de hoy (CURRENT_DATE).


-- B5. Inserta en order_items una línea del pedido 2004 con el producto 1,
-- cantidad 1 y el precio unitario que consultaste.


-- B6. Descuenta una naranja en inventory solo si queda stock suficiente.
-- Usa RETURNING para ver el stock nuevo. Debes obtener UPDATE 1 y stock 22.


-- B7. Ejecuta COMMIT si B6 devolvió UPDATE 1. Si falla, ejecuta ROLLBACK.
COMMIT;

-- B8. Ejecuta estas consultas una a una. Debes ver el pedido, su línea y stock 22.
SELECT order_id, customer_id FROM public.orders WHERE order_id = 2004;
SELECT product_id, quantity, unit_price FROM public.order_items WHERE order_id = 2004;
SELECT stock FROM public.inventory WHERE product_id = 1;

-- COMPRA FALLIDA. María intenta comprar dos cajas en el pedido 2001.

-- B9. Abre una transacción nueva.
BEGIN;

-- B10. Escribe un SELECT en inventory para consultar el stock del producto 4.
-- Comprueba que solo queda una caja y sigue para provocar el fallo.


-- B11. Escribe un SELECT en products para consultar el precio actual de la caja.


-- B12. Inserta el pedido 2001 en orders para María (customer_id = 1), con fecha de hoy.


-- B13. Inserta en order_items una línea del pedido 2001 con el producto 4,
-- cantidad 2 y el precio por caja del catálogo.


-- B14. Intenta restar dos cajas. Filtra solo por el ID del producto para que
-- el CHECK detecte el stock negativo. Detente cuando aparezca el error.


-- B15. Revierte la transacción.
ROLLBACK;

-- B16. Ejecuta cada consulta. El pedido y la línea deben tener cero filas.
-- El stock debe seguir en una caja.
SELECT COUNT(*) AS pedidos_2001 FROM public.orders WHERE order_id = 2001;
SELECT COUNT(*) AS lineas_2001 FROM public.order_items WHERE order_id = 2001;
SELECT stock FROM public.inventory WHERE product_id = 4;
