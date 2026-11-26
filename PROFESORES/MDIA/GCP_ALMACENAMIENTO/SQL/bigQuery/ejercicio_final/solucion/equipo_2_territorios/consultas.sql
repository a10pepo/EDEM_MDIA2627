-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado en EU.

-- Cifras de referencia para la escala completa con semilla 27182.

-- Cuando hay una sola consulta para varias preguntas, revisa sus columnas antes de pasar a la siguiente.

-- ¿Qué provincias realizaron pilotos comerciales en 2025?
-- Resultado esperado. Hay 10 provincias piloto. Son A Coruña, Cantabria, Girona, Granada, Illes Balears,
-- Las Palmas, Lugo, Ourense, Pontevedra y Santa Cruz de Tenerife.
-- Por qué. Cada fila de territory_monthly representa una provincia y un mes. La consulta también
-- devuelve la duración y la cobertura media para la siguiente pregunta.
SELECT province,
       COUNT(*) AS meses_de_prueba,
       ROUND(AVG(coverage_pct), 2) AS cobertura_media_pct
FROM `PROJECT_ID.terra_taronja_raw.territory_monthly`
WHERE sales_program = 'piloto' AND month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
GROUP BY province
ORDER BY province;

-- ¿Cuántos meses duró cada piloto y cuál fue su cobertura media?
-- Resultado esperado. A Coruña tuvo 12 meses de piloto y un 47,42 % de cobertura media.
-- Santa Cruz de Tenerife tuvo 11 meses y un 35,73 % de cobertura media.
-- Por qué. El número de meses mide la duración y la cobertura media describe el alcance.
-- Ambas cifras ayudan a interpretar las diferencias en pedidos.

-- ¿Cuántos pedidos se realizaron durante el piloto en cada provincia?
-- Resultado esperado. Hubo 34.428 pedidos durante el piloto de A Coruña y 22.446 durante
-- el de Santa Cruz de Tenerife.
-- Por qué. Enlazamos por provincia y mes con los registros de piloto de territory_monthly.
-- LEFT JOIN conserva los meses sin pedidos. COUNT(o.order_id) cuenta solo pedidos existentes.
-- La misma consulta devuelve los pedidos por mes y el coste para las dos preguntas siguientes.
WITH meses_piloto AS (
  SELECT province, month_start
  FROM `PROJECT_ID.terra_taronja_raw.territory_monthly`
  WHERE sales_program = 'piloto'
    AND month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
    AND province IN ('A Coruña', 'Santa Cruz de Tenerife')
)
SELECT p.province,
       COUNT(DISTINCT p.month_start) AS meses_de_piloto,
       COUNT(o.order_id) AS pedidos,
       ROUND(1.0 * COUNT(o.order_id) / COUNT(DISTINCT p.month_start), 2) AS pedidos_por_mes,
       ROUND(AVG(o.shipping_cost_cents) / 100.0, 2) AS envio_medio_eur
FROM meses_piloto p
LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
  ON o.province = p.province AND DATE_TRUNC(o.order_date, MONTH) = p.month_start
GROUP BY p.province
ORDER BY pedidos_por_mes DESC, p.province;

-- ¿Cuántos pedidos por mes de piloto consiguió cada una?
-- Resultado esperado. A Coruña consiguió 2.869 pedidos por mes. Santa Cruz de Tenerife, 2.040,55.
-- Por qué. Dividimos los pedidos entre todos los meses de piloto, incluidos los meses sin compras.
-- Así podemos comparar provincias cuyos pilotos duraron distinto tiempo.

-- ¿Cuál fue el coste medio de envío durante cada piloto?
-- Resultado esperado. El envío medio costó 7,43 € en A Coruña y 13,73 € en Santa Cruz de Tenerife.
-- Por qué. Hacemos la media por pedido dentro del piloto. La columna envio_medio_eur muestra
-- el coste para la tienda en euros.

-- ¿En cuál de las dos provincias ampliaríais la prueba y qué datos justifican vuestra propuesta?
-- Resultado esperado. Ampliaría primero A Coruña. Consiguió 2.869 pedidos por mes frente a 2.040,55
-- en Santa Cruz de Tenerife y su envío medio costó 7,43 € frente a 13,73 €.
-- Por qué. La tasa mensual tiene en cuenta la duración. A Coruña también tuvo más cobertura, así
-- que revisaría qué tal funciona el servicio en la zona adicional antes de extenderlo a toda la provincia.

-- ¿Qué podéis mirar si os queda tiempo?

-- ¿Cuál fue el tiempo medio de entrega durante cada piloto? ¿Cambiaría vuestra decisión?
-- Resultado esperado. 2,71 días en A Coruña y 5,94 días en Santa Cruz de Tenerife.
-- Mantendría la propuesta de A Coruña porque también entregó más rápido.
-- Por qué. Usamos los mismos pedidos. La fecha del pedido determina si pertenece al piloto,
-- aunque la entrega ocurra en el mes siguiente.
SELECT t.province,
       ROUND(AVG(DATE_DIFF(o.delivery_date, o.order_date, DAY)), 2) AS plazo_medio_dias
FROM `PROJECT_ID.terra_taronja_raw.territory_monthly` t
LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
  ON o.province = t.province AND DATE_TRUNC(o.order_date, MONTH) = t.month_start
WHERE t.sales_program = 'piloto'
  AND t.month_start >= DATE '2025-01-01' AND t.month_start < DATE '2026-01-01'
  AND t.province IN ('A Coruña', 'Santa Cruz de Tenerife')
GROUP BY t.province
ORDER BY plazo_medio_dias, t.province;

-- Ampliación para la puesta en común.

-- Bloque 1. ¿Qué provincias tuvieron un piloto, cuántos meses duró y qué cobertura alcanzó?
-- Por qué. Cada fila de territorio representa un mes en una provincia. Contar los meses y calcular su
-- cobertura media permite distinguir un piloto más largo o amplio de otro con más pedidos por mes.
-- Interpretación. Leed el alcance junto al volumen de pedidos. Una provincia con más meses de
-- observación tuvo más ocasiones de registrar compras.
SELECT region, province,
       COUNT(*) AS meses_de_piloto,
       SUM(qualified_contacts) AS contactos_cualificados,
       AVG(coverage_pct) AS cobertura_media_pct
FROM `PROJECT_ID.terra_taronja_raw.territory_monthly`
WHERE sales_program = 'piloto'
  AND month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
GROUP BY region, province
ORDER BY region, contactos_cualificados DESC, province;

-- Bloque 2. ¿Cómo cambia la comparación si miráis las primeras compras respecto a los contactos alcanzados?
-- Por qué. Vinculamos las primeras compras al mes y la provincia del piloto para usar compras y
-- contactos del mismo periodo. El cociente permite comparar pilotos con distinto alcance.
-- Interpretación. El cociente aproxima primeras compras por contacto. Los contactos son agregados
-- estimados y carecemos de un vínculo individual con las compras.
WITH exposicion AS (
  SELECT t.region, t.province, SUM(t.qualified_contacts) AS contactos
  FROM `PROJECT_ID.terra_taronja_raw.territory_monthly` t
  WHERE t.sales_program = 'piloto'
    AND t.month_start >= DATE '2025-01-01' AND t.month_start < DATE '2026-01-01'
  GROUP BY t.region, t.province
), altas AS (
  SELECT c.province, COUNT(*) AS primeras_compras
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN `PROJECT_ID.terra_taronja_raw.territory_monthly` t
    ON t.province = c.province AND t.month_start = DATE_TRUNC(c.first_order_date, MONTH)
  WHERE t.sales_program = 'piloto'
    AND t.month_start >= DATE '2025-01-01' AND t.month_start < DATE '2026-01-01'
  GROUP BY c.province
)
SELECT e.region, e.province, e.contactos, COALESCE(a.primeras_compras, 0) AS primeras_compras,
       100.0 * COALESCE(a.primeras_compras, 0) / NULLIF(e.contactos, 0) AS primeras_compras_por_100_contactos
FROM exposicion e
LEFT JOIN altas a USING (province)
ORDER BY primeras_compras_por_100_contactos DESC, e.province;

-- Bloque 3. ¿Qué plazo común usaríais para comparar cuántos clientes repiten después de su primera compra?
-- Por qué. La unión conserva también a quienes nunca repitieron, porque forman parte del denominador.
-- Limitamos las primeras compras a fechas que dejan 90 días completos dentro del histórico.
-- Interpretación. La última primera compra elegible es el 2 de octubre de 2025. Medimos los pedidos
-- posteriores en la misma ventana para todas las provincias.
WITH seguimiento AS (
  SELECT c.region, c.province, c.customer_id, COUNT(o.order_id) AS pedidos_posteriores
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN `PROJECT_ID.terra_taronja_raw.territory_monthly` t
    ON t.province = c.province AND t.month_start = DATE_TRUNC(c.first_order_date, MONTH)
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
    ON o.customer_id = c.customer_id
   AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 1 AND 90
  WHERE t.sales_program = 'piloto'
    AND c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
  GROUP BY c.region, c.province, c.customer_id
)
SELECT region, province, COUNT(*) AS clientes_con_90_dias,
       SUM(CASE WHEN pedidos_posteriores > 0 THEN 1 ELSE 0 END) AS clientes_que_repiten,
       100.0 * AVG(CASE WHEN pedidos_posteriores > 0 THEN 1.0 ELSE 0.0 END) AS pct_repite_90d
FROM seguimiento
GROUP BY region, province
ORDER BY pct_repite_90d DESC, province;

-- Bloque 4. ¿En qué provincias es más caro o lento entregar y cuánto queda de contribución tras los costes?
-- Por qué. Los pedidos muestran interés. El plazo y el coste medio indican cómo se atiende, y la
-- contribución incorpora también portes cobrados, coste del producto y servicio. Juntos ayudan a valorar
-- la viabilidad.
-- Interpretación. Las provincias canarias tienen envíos más caros y lentos que las gallegas, aunque
-- conservan contribución positiva.
SELECT o.region, o.province, COUNT(*) AS pedidos,
       AVG(o.shipping_cost_cents) / 100.0 AS coste_medio_envio_eur,
       AVG(DATE_DIFF(o.delivery_date, o.order_date, DAY)) AS media_dias_entrega,
       SUM(o.contribution_cents) / 100.0 AS contribucion_total_eur,
       100.0 * SUM(o.contribution_cents) / NULLIF(SUM(o.net_cents), 0) AS pct_contribucion
FROM `PROJECT_ID.terra_taronja_raw.orders` o
JOIN `PROJECT_ID.terra_taronja_raw.territory_monthly` t
  ON t.province = o.province AND t.month_start = DATE_TRUNC(o.order_date, MONTH)
WHERE t.sales_program = 'piloto'
    AND t.month_start >= DATE '2025-01-01' AND t.month_start < DATE '2026-01-01'
GROUP BY o.region, o.province
ORDER BY coste_medio_envio_eur DESC, o.province;

-- Bloque 5. ¿Qué piloto combina más repetición con un coste de envío razonable?
-- Consulta avanzada de referencia.
WITH meses_piloto AS (
  SELECT region, province, month_start, qualified_contacts
  FROM `PROJECT_ID.terra_taronja_raw.territory_monthly`
  WHERE sales_program = 'piloto'
    AND month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
), alcance AS (
  SELECT region, province, SUM(qualified_contacts) AS contactos
  FROM meses_piloto
  GROUP BY region, province
), primeras_compras AS (
  SELECT p.province, c.customer_id, c.first_order_date
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  JOIN meses_piloto p
    ON p.province = c.province AND p.month_start = DATE_TRUNC(c.first_order_date, MONTH)
), seguimiento AS (
  SELECT c.province, c.customer_id, COUNT(o.order_id) AS pedidos_posteriores
  FROM primeras_compras c
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
    ON o.customer_id = c.customer_id
   AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 1 AND 90
  WHERE c.first_order_date <= DATE '2025-10-02'
  GROUP BY c.province, c.customer_id
), altas AS (
  SELECT province, COUNT(*) AS primeras
  FROM primeras_compras
  GROUP BY province
), repeticion AS (
  SELECT province, COUNT(*) AS elegibles,
         SUM(CASE WHEN pedidos_posteriores > 0 THEN 1 ELSE 0 END) AS repiten
  FROM seguimiento
  GROUP BY province
), operacion AS (
  SELECT p.province, COUNT(*) AS pedidos, SUM(o.shipping_cost_cents) AS envio_centimos,
         SUM(DATE_DIFF(o.delivery_date, o.order_date, DAY)) AS dias_entrega,
         SUM(o.contribution_cents) AS contribucion_centimos, SUM(o.net_cents) AS neto_centimos
  FROM `PROJECT_ID.terra_taronja_raw.orders` o
  JOIN meses_piloto p
    ON p.province = o.province AND p.month_start = DATE_TRUNC(o.order_date, MONTH)
  GROUP BY p.province
), por_provincia AS (
  SELECT a.region, a.province, a.contactos, COALESCE(b.primeras, 0) AS primeras,
         COALESCE(r.elegibles, 0) AS elegibles, COALESCE(r.repiten, 0) AS repiten,
         COALESCE(o.pedidos, 0) AS pedidos, COALESCE(o.envio_centimos, 0) AS envio_centimos,
         COALESCE(o.dias_entrega, 0) AS dias_entrega,
         COALESCE(o.contribucion_centimos, 0) AS contribucion_centimos,
         COALESCE(o.neto_centimos, 0) AS neto_centimos
  FROM alcance a
  LEFT JOIN altas b ON b.province = a.province
  LEFT JOIN repeticion r ON r.province = a.province
  LEFT JOIN operacion o ON o.province = a.province
), resumen AS (
  SELECT 'provincia' AS level, region, province AS territory, contactos, primeras, elegibles, repiten,
         pedidos, envio_centimos, dias_entrega, contribucion_centimos, neto_centimos
  FROM por_provincia
  UNION ALL
  SELECT 'comunidad', region, region, SUM(contactos), SUM(primeras), SUM(elegibles), SUM(repiten),
         SUM(pedidos), SUM(envio_centimos), SUM(dias_entrega), SUM(contribucion_centimos), SUM(neto_centimos)
  FROM por_provincia
  GROUP BY region
)
SELECT level, region, territory, pedidos AS orders, elegibles AS eligible,
       1.0 * primeras / NULLIF(contactos, 0) AS first_orders_per_contact,
       1.0 * repiten / NULLIF(elegibles, 0) AS repeat_90d,
       envio_centimos / 100.0 / NULLIF(pedidos, 0) AS shipping_eur_per_order,
       1.0 * dias_entrega / NULLIF(pedidos, 0) AS delivery_days_per_order,
       1.0 * contribucion_centimos / NULLIF(neto_centimos, 0) AS contribution_rate
FROM resumen
ORDER BY level, region, territory;

-- Bloque 6. ¿Dónde ampliaríais el piloto y qué podéis concluir sobre las zonas donde aún no hubo actividad?
-- Por qué. La recomendación combina las señales del bloque anterior. Galicia ofrece más repetición y un
-- coste de envío menor que Canarias. El registro de cobertura delimita dónde pudimos observar compras.
-- Interpretación. Ampliaría primero Galicia y mantendría Canarias como segundo piloto con objetivos de
-- coste y plazo. Para estimar la demanda en zonas sin actividad necesitaríamos un piloto u otra fuente.
WITH pedidos_por_mes AS (
  SELECT province, DATE_TRUNC(order_date, MONTH) AS mes, COUNT(*) AS pedidos
  FROM `PROJECT_ID.terra_taronja_raw.orders`
  WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
  GROUP BY province, mes
)
SELECT t.region, t.province, t.sales_program,
       COUNT(*) AS meses_con_registro,
       SUM(CASE WHEN o.pedidos > 0 THEN 1 ELSE 0 END) AS meses_con_pedidos,
       AVG(t.coverage_pct) AS cobertura_media_pct,
       SUM(COALESCE(o.pedidos, 0)) AS pedidos_observados
FROM `PROJECT_ID.terra_taronja_raw.territory_monthly` t
LEFT JOIN pedidos_por_mes o ON o.province = t.province AND o.mes = t.month_start
WHERE t.month_start >= DATE '2025-01-01' AND t.month_start < DATE '2026-01-01'
GROUP BY t.region, t.province, t.sales_program
ORDER BY t.region, t.province, t.sales_program;
