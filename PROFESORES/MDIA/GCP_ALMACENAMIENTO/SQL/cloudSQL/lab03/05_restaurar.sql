-- Cierra las transacciones de A y B antes de ejecutar el bloque completo.
DO $restaurar$
BEGIN
    IF current_database() <> 'terra_taronja' THEN
        RAISE EXCEPTION 'Restauración bloqueada en la base %. Conéctate a terra_taronja.', current_database();
    END IF;

    DELETE FROM public.order_items WHERE order_id IN (2001, 2002, 2003, 2004);
    DELETE FROM public.orders WHERE order_id IN (2001, 2002, 2003, 2004);

    UPDATE public.inventory AS i
    SET stock = e.stock
    FROM (VALUES (1, 24), (4, 1)) AS e (product_id, stock)
    WHERE i.product_id = e.product_id;
END;
$restaurar$;
