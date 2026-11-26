-- Ejecuta el archivo completo después de crear las tablas.
BEGIN;

INSERT INTO public.customers (customer_id, name, email) VALUES
    (1, 'María', 'maria@example.com'),
    (2, 'Juan', 'juan@example.com');

INSERT INTO public.products (product_id, name, price) VALUES
    (1, 'Naranja', 2.50),
    (2, 'Zumo de naranja', 8.00),
    (3, 'Mermelada de naranja', 4.00),
    (4, 'Caja de naranjas de temporada', 12.00),
    (5, 'Horchata', 3.50),
    (6, 'Arroz bomba Albufera DOP', 2.00);

INSERT INTO public.orders (order_id, customer_id, order_date) VALUES
    (1001, 1, DATE '2026-10-01'),
    (1002, 2, DATE '2026-10-02'),
    (1003, 1, DATE '2026-10-03'),
    (1004, 2, DATE '2026-10-04');

-- unit_price conserva el precio por unidad registrado al realizar el pedido.
INSERT INTO public.order_items (order_id, product_id, quantity, unit_price) VALUES
    (1001, 1, 2, 5.50),
    (1001, 2, 2, 3.00),
    (1002, 2, 1, 3.00),
    (1002, 3, 2, 4.00),
    (1003, 5, 2, 3.50),
    (1003, 6, 1, 2.00),
    (1004, 1, 1, 2.50),
    (1004, 6, 2, 2.00);

-- Son las existencias disponibles al iniciar el lab.
INSERT INTO public.inventory (product_id, stock) VALUES
    (1, 24),
    (2, 18),
    (3, 12),
    (4, 1),
    (5, 15),
    (6, 10);

COMMIT;
