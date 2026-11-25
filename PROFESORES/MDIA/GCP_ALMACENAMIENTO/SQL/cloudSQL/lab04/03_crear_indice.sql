DO $indice$
BEGIN
    IF current_database() <> 'terra_taronja' THEN
        RAISE EXCEPTION 'Ejecuta esta práctica en la base terra_taronja.';
    END IF;

    IF (
        SELECT col_description(attrelid, attnum)
        FROM pg_catalog.pg_attribute
        WHERE attrelid = 'public.orders'::regclass AND attname = 'created_at' AND NOT attisdropped
    ) IS DISTINCT FROM 'Terra Taronja Lab 4 datos sintéticos' THEN
        RAISE EXCEPTION 'Prepara los datos de la práctica antes de crear el índice.';
    END IF;

    CREATE INDEX idx_orders_created_at ON public.orders USING btree (created_at);
    COMMENT ON INDEX public.idx_orders_created_at IS 'Terra Taronja Lab 4 índice de rendimiento';
END;
$indice$;
