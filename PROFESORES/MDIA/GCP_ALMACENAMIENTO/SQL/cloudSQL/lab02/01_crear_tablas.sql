-- Escribe una sentencia CREATE TABLE debajo de cada bloque.
-- Crea las tablas en el esquema public, en el orden indicado.
-- Todas las columnas son obligatorias. Usa los nombres y tipos indicados
-- para que el script de datos iniciales pueda cargar los ejemplos.

-- 1. customers
-- customer_id (INTEGER) es la clave primaria.
-- name (TEXT) guarda el nombre del cliente.
-- email (TEXT) guarda el correo y debe ser único.


-- 2. products
-- product_id (INTEGER) es la clave primaria.
-- name (TEXT) guarda el nombre del producto.
-- price (NUMERIC(10, 2)) guarda el precio actual en euros y debe ser >= 0.


-- 3. orders
-- order_id (INTEGER) es la clave primaria.
-- customer_id (INTEGER) es una clave foránea a customers.customer_id.
-- order_date (DATE) guarda la fecha del pedido.


-- 4. order_items
-- order_id (INTEGER) es una clave foránea a orders.order_id.
-- product_id (INTEGER) es una clave foránea a products.product_id.
-- La combinación de order_id y product_id es la clave primaria.
-- quantity (INTEGER) guarda el número de unidades y debe ser > 0.
-- unit_price (NUMERIC(10, 2)) guarda el precio por unidad del pedido en euros
-- y debe ser >= 0.


-- 5. inventory
-- product_id (INTEGER) es la clave primaria y también una clave foránea
-- a products.product_id.
-- stock (INTEGER) guarda las unidades disponibles y debe ser >= 0.
