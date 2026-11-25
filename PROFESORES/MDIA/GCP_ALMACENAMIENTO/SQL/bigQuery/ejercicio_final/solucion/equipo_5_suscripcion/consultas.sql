-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado en EU.

-- Cifras de referencia para la escala completa con semilla 27182.

-- Cuando hay una sola consulta para varias preguntas, revisa sus columnas antes de pasar a la siguiente.

-- ¿Cuántos pedidos realizaron los clientes particulares en 2025 en dos provincias que elijáis?
-- Resultado esperado. Con Valencia y Girona como ejemplo, hubo 94.023 pedidos de particulares en
-- Valencia y 11.624 en Girona.
-- Por qué. Contar pedidos da el volumen. La misma consulta devuelve clientes distintos y pedidos por
-- cliente para las dos preguntas siguientes.
SELECT province, COUNT(*) AS pedidos,
       COUNT(DISTINCT customer_id) AS clientes,
       ROUND(1.0 * COUNT(*) / NULLIF(COUNT(DISTINCT customer_id), 0), 2) AS pedidos_por_cliente
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE customer_type = 'particular' AND order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
  AND province IN ('Valencia', 'Girona')
GROUP BY province
ORDER BY pedidos_por_cliente DESC, province;

-- ¿Cuántos clientes distintos realizaron esos pedidos en cada provincia?
-- Resultado esperado. Compraron 27.388 particulares distintos en Valencia y 5.547 en Girona.
-- Por qué. Un cliente puede hacer varios pedidos. Contarlo una sola vez da el denominador de la
-- comparación.

-- ¿Cuál es la media de pedidos por cliente en cada provincia?
-- Resultado esperado. Valencia obtiene 3,43 pedidos por cliente y Girona 2,10.
-- Por qué. Dividir por clientes hace comparables provincias con tamaños distintos.

-- ¿Cuántos clientes realizaron compras en al menos dos meses diferentes de 2025 en cada provincia?
-- Resultado esperado. En Valencia compraron en al menos dos meses 17.202 clientes. En Girona, 2.441.
-- Por qué. Agrupamos por provincia y cliente y contamos meses distintos. Así un cliente con varios
-- pedidos en el mismo mes cuenta un solo mes. La última columna sirve para la pregunta opcional.
WITH meses_por_cliente AS (
  SELECT province, customer_id,
         COUNT(DISTINCT DATE_TRUNC(order_date, MONTH)) AS meses_con_pedidos
  FROM `PROJECT_ID.terra_taronja_raw.orders`
  WHERE customer_type = 'particular' AND order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
    AND province IN ('Valencia', 'Girona')
  GROUP BY province, customer_id
), resumen AS (
  SELECT province, COUNT(*) AS clientes,
         SUM(CASE WHEN meses_con_pedidos >= 2 THEN 1 ELSE 0 END) AS clientes_en_varios_meses
  FROM meses_por_cliente
  GROUP BY province
)
SELECT province, clientes, clientes_en_varios_meses,
       ROUND(100.0 * clientes_en_varios_meses / NULLIF(clientes, 0), 2) AS pct_en_varios_meses
FROM resumen
ORDER BY province;

-- ¿En cuál de las dos provincias probaríais un servicio de entregas periódicas y qué datos lo justifican?
-- Resultado esperado. Probaría primero en Valencia. Tuvo 3,43 pedidos por cliente frente a 2,10
-- en Girona y 17.202 clientes compraron en dos meses o más, frente a 2.441 en Girona.
-- Por qué. La media indica la frecuencia de compra y los meses distintos muestran repetición
-- a lo largo del año. Una prueba permitiría medir si los clientes aceptarían el servicio.

-- ¿Qué podéis mirar si os queda tiempo?

-- ¿Qué porcentaje de clientes compró en al menos dos meses distintos? ¿Cambia vuestra recomendación?
-- Resultado esperado. El 62,81 % en Valencia y el 44,01 % en Girona. Mantendría la propuesta
-- de Valencia porque la proporción también es mayor.
-- Por qué. Dividimos los clientes con compras en varios meses entre todos los particulares con
-- pedidos en 2025 de su provincia. El porcentaje permite comparar bases de distinto tamaño.

-- Ampliación para la puesta en común.

-- Bloque 1. ¿En qué provincias repiten más los particulares y qué ventana usaríais para compararlos?
-- Por qué. Igualamos los días observados desde la primera compra porque los clientes empiezan en fechas
-- distintas. El denominador incluye a quienes compraron una sola vez.
-- Interpretación. Valencia y Castellón registran más repetición que Girona en la ventana de 90 días.
WITH seguimiento AS (
  SELECT c.province, c.customer_id, COUNT(o.order_id) AS pedidos_posteriores
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
    ON o.customer_id = c.customer_id
   AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 1 AND 90
  WHERE c.customer_type = 'particular'
    AND c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
  GROUP BY c.province, c.customer_id
)
SELECT province, COUNT(*) AS clientes_con_90_dias,
       SUM(CASE WHEN pedidos_posteriores > 0 THEN 1 ELSE 0 END) AS clientes_que_repiten,
       100.0 * AVG(CASE WHEN pedidos_posteriores > 0 THEN 1.0 ELSE 0.0 END) AS pct_repite_90d
FROM seguimiento
GROUP BY province
ORDER BY pct_repite_90d DESC, province;

-- Bloque 2. ¿Cuántos días suelen pasar entre pedidos de un mismo cliente?
-- Por qué. Usamos el pedido inmediatamente anterior para medir cada intervalo real. Promediamos primero
-- por cliente para que los compradores que hacen más pedidos no pesen más.
-- Interpretación. El resultado describe el ritmo típico de quienes repiten. La dispersión del siguiente
-- bloque ayuda a valorar si ese ritmo es regular.
WITH compras_90_dias AS (
  SELECT c.province, o.customer_id, o.order_id, o.order_date
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (customer_id)
  WHERE c.customer_type = 'particular'
    AND c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
    AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 0 AND 90
), secuencia AS (
  SELECT province, customer_id, order_date,
         LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS fecha_anterior
  FROM compras_90_dias
), intervalos AS (
  SELECT province, customer_id, DATE_DIFF(order_date, fecha_anterior, DAY) AS dias
  FROM secuencia
  WHERE fecha_anterior IS NOT NULL
), frecuencia AS (
  SELECT province, customer_id, AVG(1.0 * dias) AS intervalo_medio_cliente
  FROM intervalos
  GROUP BY province, customer_id
)
SELECT province, COUNT(*) AS clientes_que_repiten,
       AVG(intervalo_medio_cliente) AS intervalo_medio_dias
FROM frecuencia
GROUP BY province
ORDER BY intervalo_medio_dias, province;

-- Bloque 3. ¿Cómo distinguiríais a quien compra con regularidad de quien tiene el mismo intervalo medio con compras esporádicas?
-- Por qué. La desviación indica cuánto varían los intervalos alrededor de su media. Dividirla por la
-- media permite comparar ritmos distintos. Pedimos tres intervalos como mínimo para observar variación.
-- Interpretación. Por ejemplo, 30, 30 y 30 días tienen la misma media que 10, 30 y 50 días. La segunda
-- secuencia tiene más dispersión.
WITH compras_90_dias AS (
  SELECT c.province, o.customer_id, o.order_id, o.order_date
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (customer_id)
  WHERE c.customer_type = 'particular'
    AND c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
    AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 0 AND 90
), secuencia AS (
  SELECT province, customer_id, order_date,
         LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS fecha_anterior
  FROM compras_90_dias
), intervalos AS (
  SELECT province, customer_id, DATE_DIFF(order_date, fecha_anterior, DAY) AS dias
  FROM secuencia
  WHERE fecha_anterior IS NOT NULL
)
SELECT province, customer_id, COUNT(*) AS intervalos,
       AVG(1.0 * dias) AS intervalo_medio_dias,
       STDDEV_POP(dias) AS dispersion_dias,
       STDDEV_POP(dias) / NULLIF(AVG(1.0 * dias), 0) AS dispersion_relativa
FROM intervalos
GROUP BY province, customer_id
HAVING COUNT(*) >= 3
ORDER BY province, ROUND(intervalo_medio_dias), dispersion_dias, customer_id;

-- Bloque 4. ¿Qué proporción de los productos de una cesta aparece también en la compra anterior?
-- Por qué. Comparamos los identificadores de producto entre compras consecutivas y dividimos por el
-- tamaño de la cesta actual. Esa proporción permite comparar cestas grandes y pequeñas por igual.
-- Interpretación. Si dos de cuatro productos de la cesta actual estaban en la anterior, la coincidencia
-- es del 50 %. El promedio final da el mismo peso a cada cliente.
WITH compras_90_dias AS (
  SELECT c.province, o.customer_id, o.order_id, o.order_date
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (customer_id)
  WHERE c.customer_type = 'particular'
    AND c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
    AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 0 AND 90
), secuencia AS (
  SELECT province, customer_id, order_id,
         LAG(order_id) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS pedido_anterior
  FROM compras_90_dias
), coincidencias AS (
  SELECT s.province, s.customer_id, s.order_id,
         COUNT(*) AS productos_cesta_actual,
         COUNT(a.product_id) AS productos_repetidos
  FROM secuencia s
  JOIN `PROJECT_ID.terra_taronja_raw.order_items` i ON i.order_id = s.order_id
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.order_items` a
    ON a.order_id = s.pedido_anterior AND a.product_id = i.product_id
  WHERE s.pedido_anterior IS NOT NULL
  GROUP BY s.province, s.customer_id, s.order_id
), resumen_cliente AS (
  SELECT province, customer_id,
         AVG(100.0 * productos_repetidos / productos_cesta_actual) AS pct_repetidos
  FROM coincidencias
  GROUP BY province, customer_id
)
SELECT province, COUNT(*) AS clientes_con_cestas_comparables,
       AVG(pct_repetidos) AS pct_medio_productos_repetidos
FROM resumen_cliente
GROUP BY province
ORDER BY pct_medio_productos_repetidos DESC, province;

-- Bloque 5. ¿Qué provincias combinan repetición, intervalos regulares y cestas parecidas?
-- Consulta avanzada de referencia.
-- Por qué. Combinamos frecuencia, regularidad y coincidencia de productos porque una suscripción
-- necesita un ritmo y una cesta previsibles. Dividimos por toda la cohorte para estimar qué parte de los
-- clientes cumple los criterios.
-- Interpretación. Valencia y Castellón rondan un tercio de la cohorte con esta definición.
WITH eligible AS (
  SELECT customer_id, province, region, first_order_date
  FROM `PROJECT_ID.terra_taronja_raw.customers`
  WHERE customer_type = 'particular'
    AND first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
), sequence AS (
  SELECT o.customer_id, o.order_id, o.order_date,
         LAG(o.order_id) OVER customer_orders AS previous_id,
         LAG(o.order_date) OVER customer_orders AS previous_date
  FROM `PROJECT_ID.terra_taronja_raw.orders` o
  JOIN eligible c USING (customer_id)
  WHERE DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 0 AND 90
  WINDOW customer_orders AS (PARTITION BY o.customer_id ORDER BY o.order_date, o.order_id)
), pairs AS (
  SELECT s.customer_id, s.order_id, DATE_DIFF(s.order_date, s.previous_date, DAY) AS gap_days,
         COUNT(*) AS items, COUNT(prev.product_id) AS shared_items
  FROM sequence s
  JOIN `PROJECT_ID.terra_taronja_raw.order_items` cur ON cur.order_id = s.order_id
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.order_items` prev
    ON prev.order_id = s.previous_id AND prev.product_id = cur.product_id
  WHERE s.previous_id IS NOT NULL
  GROUP BY s.customer_id, s.order_id, s.order_date, s.previous_date
), metrics AS (
  SELECT customer_id, COUNT(*) AS intervals, AVG(1.0 * gap_days) AS gap_days,
         AVG(1.0 * gap_days * gap_days) AS mean_square_days,
         AVG(1.0 * shared_items / items) AS basket_overlap
  FROM pairs
  GROUP BY customer_id
)
SELECT c.region, c.province, COUNT(*) AS eligible_customers,
       AVG(CASE WHEN m.intervals > 0 THEN 1.0 ELSE 0.0 END) AS repeat_90d,
       AVG(m.gap_days) AS mean_gap_among_repeat_buyers,
       AVG(m.basket_overlap) AS basket_overlap_among_repeat_buyers,
       AVG(CASE WHEN m.intervals >= 3 AND m.gap_days BETWEEN 10 AND 35
                 AND m.mean_square_days - m.gap_days * m.gap_days <= 0.06 * m.gap_days * m.gap_days
                 AND m.basket_overlap >= 0.55 THEN 1.0 ELSE 0.0 END) AS regular_basket_share
FROM eligible c
LEFT JOIN metrics m USING (customer_id)
GROUP BY c.region, c.province
ORDER BY regular_basket_share DESC, c.province;

-- Bloque 6. ¿Dónde probaríais una suscripción y qué os falta saber sobre el interés de los clientes?
-- Por qué. La regularidad indica dónde merece la pena probar. La cesta y el coste de envío del bloque
-- final ayudan a valorar la viabilidad. El histórico no registra si los clientes aceptarían una cuota o
-- una frecuencia fija.
-- Interpretación. Probaría en Valencia o Castellón. En el piloto mediría aceptación, frecuencia elegida,
-- disposición a pagar y margen del servicio.
SELECT province, COUNT(DISTINCT customer_id) AS particulares_activos,
       COUNT(*) AS pedidos, AVG(net_cents) / 100.0 AS cesta_neta_media_eur,
       AVG(shipping_cost_cents) / 100.0 AS envio_medio_eur,
       100.0 * SUM(contribution_cents) / NULLIF(SUM(net_cents), 0) AS pct_contribucion
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE customer_type = 'particular' AND order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY province
ORDER BY particulares_activos DESC, province;
