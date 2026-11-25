-- A1. Baja temporalmente de 24 a 23 el stock de la naranja (producto 1).
BEGIN;

UPDATE public.inventory
SET stock = stock - 1
WHERE product_id = 1 AND stock = 24
RETURNING product_id, stock;

-- PAUSA. Dentro de la transacción, el stock es 23.

-- A2. Deshaz el cambio y comprueba que el stock vuelve a 24.
ROLLBACK;

SELECT product_id, stock FROM public.inventory WHERE product_id = 1;

-- A3. Repite la misma operación en una transacción nueva.
BEGIN;

UPDATE public.inventory
SET stock = stock - 1
WHERE product_id = 1 AND stock = 24
RETURNING product_id, stock;

-- A4. Confirma el cambio y comprueba que el stock sigue en 23.
COMMIT;

SELECT product_id, stock FROM public.inventory WHERE product_id = 1;
