-- Sustituye PROJECT_ID. Ejecuta cada bloque por separado.

-- 1. Tabla original, con todas las columnas.
SELECT *
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-09-01' AND order_date < DATE '2025-10-01'
  AND province = 'Valencia' AND customer_type = 'particular';

-- 2. Misma tabla y filtro, con las columnas necesarias.
SELECT order_id, order_date, net_cents
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-09-01' AND order_date < DATE '2025-10-01'
  AND province = 'Valencia' AND customer_type = 'particular';

-- 3. Repite la consulta sobre la tabla particionada.
SELECT order_id, order_date, net_cents
FROM `PROJECT_ID.terra_taronja_analitica.orders_partitioned`
WHERE order_date >= DATE '2025-09-01' AND order_date < DATE '2025-10-01'
  AND province = 'Valencia' AND customer_type = 'particular';

-- 4. Repite la consulta añadiendo clustering a la tabla.
SELECT order_id, order_date, net_cents
FROM `PROJECT_ID.terra_taronja_analitica.orders_optimized`
WHERE order_date >= DATE '2025-09-01' AND order_date < DATE '2025-10-01'
  AND province = 'Valencia' AND customer_type = 'particular';
