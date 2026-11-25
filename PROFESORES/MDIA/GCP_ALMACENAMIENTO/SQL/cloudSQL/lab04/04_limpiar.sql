DO $limpiar$
DECLARE
    columna SMALLINT;
    indice REGCLASS;
BEGIN
    IF current_database() <> 'terra_taronja' THEN
        RAISE EXCEPTION 'Limpieza bloqueada. Conéctate a terra_taronja.';
    END IF;

    LOCK TABLE public.orders IN ACCESS EXCLUSIVE MODE;

    SELECT attnum INTO columna
    FROM pg_catalog.pg_attribute
    WHERE attrelid = 'public.orders'::regclass AND attname = 'created_at' AND NOT attisdropped;

    IF NOT FOUND THEN
        RAISE NOTICE 'La práctica ya está limpia.';
        RETURN;
    END IF;

    IF col_description('public.orders'::regclass, columna)
        IS DISTINCT FROM 'Terra Taronja Lab 4 datos sintéticos' THEN
        RAISE EXCEPTION 'La columna created_at no pertenece a esta práctica.';
    END IF;

    IF EXISTS (
        SELECT 1 FROM public.orders
        WHERE created_at IS NOT NULL AND order_id NOT BETWEEN 1000000 AND 1049999
    ) THEN
        RAISE EXCEPTION 'Hay pedidos fuera del rango del lab que utilizan created_at.';
    END IF;

    indice := to_regclass('public.idx_orders_created_at');
    IF indice IS NOT NULL THEN
        IF obj_description(indice, 'pg_class')
            IS DISTINCT FROM 'Terra Taronja Lab 4 índice de rendimiento' THEN
            RAISE EXCEPTION 'El índice idx_orders_created_at no pertenece a esta práctica.';
        END IF;
        DROP INDEX public.idx_orders_created_at;
    END IF;

    -- PostgreSQL también elimina ciertos objetos dependientes al quitar una columna.
    -- El índice de la práctica ya se ha tratado. Conserva cualquier otra dependencia.
    IF EXISTS (
        SELECT 1 FROM pg_catalog.pg_depend
        WHERE refclassid = 'pg_catalog.pg_class'::regclass
          AND refobjid = 'public.orders'::regclass AND refobjsubid = columna
    ) THEN
        RAISE EXCEPTION 'Hay otros objetos que dependen de orders.created_at.';
    END IF;

    DELETE FROM public.orders
    WHERE order_id BETWEEN 1000000 AND 1049999 AND created_at IS NOT NULL;

    ALTER TABLE public.orders DROP COLUMN created_at RESTRICT;
    ANALYZE public.orders;
END;
$limpiar$;
