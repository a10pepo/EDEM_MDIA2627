-- Reinicio opcional y destructivo. Ejecuta el bloque entero en tu base de prácticas.
DO $reinicio$
BEGIN
    IF current_database() <> 'terra_taronja' THEN
        RAISE EXCEPTION 'Reinicio bloqueado en la base %. Conéctate a terra_taronja.', current_database();
    END IF;

    DROP TABLE IF EXISTS
        public.order_items,
        public.orders,
        public.inventory,
        public.products,
        public.customers
    RESTRICT;
END;
$reinicio$;
