-- Usa tu Project ID. Ejecuta cada consulta por separado con ubicación EU.
-- Con la escala y semilla del lab se esperan 1.200.000 pedidos, 3.635.172 líneas
-- y 1.200.000 filas en cada copia de pedidos.
SELECT
  (SELECT COUNT(*) FROM `PROJECT_ID.terra_taronja_raw.orders`) AS pedidos,
  (SELECT COUNT(*) FROM `PROJECT_ID.terra_taronja_raw.order_items`) AS lineas,
  (SELECT COUNT(*) FROM `PROJECT_ID.terra_taronja_analitica.orders_partitioned`) AS particionados,
  (SELECT COUNT(*) FROM `PROJECT_ID.terra_taronja_analitica.orders_optimized`) AS optimizados;

-- Ampliación opcional. Crea una copia sin particiones, con clustering.
CREATE OR REPLACE TABLE `PROJECT_ID.terra_taronja_analitica.orders_clustered`
CLUSTER BY province, customer_type AS
SELECT * FROM `PROJECT_ID.terra_taronja_raw.orders`;

-- Compara los bytes procesados por estas dos consultas con la caché desactivada.
-- Ambas devuelven los mismos pedidos y el mismo neto para el filtro indicado.
SELECT COUNT(*) AS pedidos, SUM(net_cents) AS neto_centimos
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE province = 'Castellón' AND customer_type = 'restaurante';

SELECT COUNT(*) AS pedidos, SUM(net_cents) AS neto_centimos
FROM `PROJECT_ID.terra_taronja_analitica.orders_clustered`
WHERE province = 'Castellón' AND customer_type = 'restaurante';
