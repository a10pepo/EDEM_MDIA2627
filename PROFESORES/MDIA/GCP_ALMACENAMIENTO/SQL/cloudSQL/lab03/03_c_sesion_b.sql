SET application_name = 'terra-lab3-B';

-- C2. Empieza solo cuando A haya descontado su unidad y siga sin confirmar.
-- Juan intenta comprar una caja del producto 4. Empieza la transacción.
BEGIN ISOLATION LEVEL READ COMMITTED;

-- Reutiliza B2 a B5 de la compra confirmada del archivo 02.

-- B2. Consulta el stock del producto 4 en inventory con un SELECT normal.

-- B3. Consulta el precio actual del producto 4 en products.

-- B4. Registra el pedido 2003 de Juan (customer_id = 2), con fecha de hoy.

-- B5. Añade al pedido una línea de una caja al precio que consultaste.

-- B14 adaptado. Intenta restar una caja y filtra solo por el ID del producto.
-- Aplica el mismo descuento de la compra fallida del 02, ahora de una unidad.


-- PAUSA. Cuando el descuento se quede esperando, vuelve a A para C3 y C4.


-- C5. Cuando A confirme, el descuento de B intenta dejar el stock en -1.
-- Lee el ERROR del CHECK. Reutiliza B15 para revertir la compra y comprueba
-- que se deshicieron el pedido 2003 y su línea.

ROLLBACK;

SELECT COUNT(*) AS pedidos_2003 FROM public.orders WHERE order_id = 2003;
SELECT COUNT(*) AS lineas_2003 FROM public.order_items WHERE order_id = 2003;
