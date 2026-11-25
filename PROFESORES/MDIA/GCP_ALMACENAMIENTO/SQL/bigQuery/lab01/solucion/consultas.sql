-- Lab 1 · Soluciones y resultados de referencia.
-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado.

-- 0. Comprueba que el CSV se ha cargado una sola vez.
-- Resultado esperado. 980 líneas y 320 pedidos.
SELECT COUNT(*) AS lineas,
       COUNT(DISTINCT order_id) AS pedidos,
       MIN(order_date) AS primer_dia,
       MAX(order_date) AS ultimo_dia
FROM `PROJECT_ID.terra_taronja_lab01.ventas`;

-- 1. Pedidos de 2025 por provincia de destino.
-- Resultado esperado. Valencia (37), Madrid (27) y Alicante (16) encabezan el recuento.
SELECT province AS destino,
       COUNT(DISTINCT order_id) AS pedidos
FROM `PROJECT_ID.terra_taronja_lab01.ventas`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY province
ORDER BY pedidos DESC, destino;

-- 2a. Los tres productos con más unidades en toda la muestra.
-- Resultado esperado. El arroz bomba de Sueca encabeza el ranking con 278 unidades.
SELECT product_name AS producto,
       SUM(quantity) AS unidades
FROM `PROJECT_ID.terra_taronja_lab01.ventas`
GROUP BY product_name
ORDER BY unidades DESC, producto
LIMIT 3;

-- 2b. Repite el ranking con el ingreso neto para comparar el orden.
-- Resultado esperado. La caja de cítricos de la Ribera encabeza el ranking con 2.273,33 €.
SELECT product_name AS producto,
       SUM(line_net_cents) / 100.0 AS euros_netos
FROM `PROJECT_ID.terra_taronja_lab01.ventas`
GROUP BY product_name
ORDER BY euros_netos DESC, producto
LIMIT 3;

-- 3. Provincias de origen y destinos a los que se enviaron sus productos.
-- Resultado esperado. Alicante, Castellón y Valencia aparecen con varios destinos.
SELECT origin_province AS origen,
       province AS destino,
       SUM(quantity) AS unidades
FROM `PROJECT_ID.terra_taronja_lab01.ventas`
GROUP BY origin_province, province
ORDER BY origen, destino;

-- 4. Meses de 2025 por ingreso neto. El mayor aparece primero.
-- Resultado esperado. Octubre de 2025, con 1.347,80 €.
SELECT DATE_TRUNC(order_date, MONTH) AS mes,
       SUM(line_net_cents) / 100.0 AS euros_netos
FROM `PROJECT_ID.terra_taronja_lab01.ventas`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY mes
ORDER BY euros_netos DESC, mes;
