-- Ejecuta el archivo completo en la base terra_taronja.
BEGIN;

CREATE TABLE public.customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE public.products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
);

CREATE TABLE public.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES public.customers (customer_id),
    order_date DATE NOT NULL
);

CREATE TABLE public.order_items (
    order_id INTEGER REFERENCES public.orders (order_id),
    product_id INTEGER REFERENCES public.products (product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE public.inventory (
    product_id INTEGER PRIMARY KEY REFERENCES public.products (product_id),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);

COMMIT;
