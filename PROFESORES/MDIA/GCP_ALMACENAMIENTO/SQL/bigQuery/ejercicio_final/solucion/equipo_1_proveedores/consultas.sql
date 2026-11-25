-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado en EU.

-- Cifras de referencia para la escala completa con semilla 27182.
-- requested_units mide unidades solicitadas para aprovisionamiento.

-- Cuando hay una sola consulta para varias preguntas, revisa sus columnas antes de pasar a la siguiente.

-- ¿Cuántas unidades se solicitaron y cuántas se sirvieron de cada producto durante 2025?
-- Resultado esperado. Para el producto 1 se solicitaron 552.548 unidades y se sirvieron 483.690.
-- Por qué. Sumamos los registros de cada producto a lo largo del año. La misma consulta da la
-- diferencia y el porcentaje de cumplimiento para las dos preguntas siguientes.
SELECT product_id,
       SUM(requested_units) AS unidades_solicitadas,
       SUM(fulfilled_units) AS unidades_servidas,
       SUM(requested_units - fulfilled_units) AS unidades_sin_servir,
       ROUND(100.0 * SUM(fulfilled_units) / NULLIF(SUM(requested_units), 0), 2) AS cumplimiento_pct
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly`
WHERE month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
GROUP BY product_id
ORDER BY unidades_sin_servir DESC, product_id;

-- ¿Qué producto presenta la mayor diferencia entre unidades solicitadas y servidas?
-- Resultado esperado. El producto 1 tiene la mayor diferencia, con 68.858 unidades sin servir.
-- Por qué. La resta mide cuántas unidades de aprovisionamiento quedaron sin servir. Para estimar
-- ventas perdidas harían falta datos sobre pedidos de clientes que quedaron sin atender.

-- ¿Qué porcentaje de las unidades solicitadas se sirvió para ese producto?
-- Resultado esperado. Se sirvió el 87,54 % de lo solicitado para el producto 1. Buscad el valor
-- en cumplimiento_pct.
-- Por qué. Dividimos el total servido por el total solicitado. El porcentaje permite comparar
-- productos con distinto volumen de aprovisionamiento.

-- ¿Cuál es el nombre del producto y qué cifras utilizaríais para explicar el problema?
-- Resultado esperado. Naranja de Carcaixent. Citaría las 68.858 unidades sin servir y el 87,54 %
-- de cumplimiento.
-- Por qué. La brecha muestra el volumen del problema y el porcentaje indica su gravedad relativa.
SELECT product_id, product_name
FROM `PROJECT_ID.terra_taronja_raw.products`
WHERE product_id = 1;

-- ¿En qué meses se repite el problema y qué os indica eso sobre si es puntual o recurrente?
-- Resultado esperado. Quedaron unidades sin servir en los 12 meses. Marzo fue el peor, con 17.383,
-- seguido de noviembre con 10.816. El problema es recurrente.
-- Por qué. Mirar mes a mes permite distinguir un problema repetido de un solo pico.
SELECT month_start AS mes,
       SUM(requested_units - fulfilled_units) AS unidades_sin_servir
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly`
WHERE product_id = 1 AND month_start >= DATE '2025-01-01' AND month_start < DATE '2026-01-01'
GROUP BY mes
ORDER BY mes;

-- ¿Qué podéis mirar si os queda tiempo?

-- ¿Qué proveedor concentra más unidades sin servir para ese producto y cuál tiene menor cumplimiento?
-- Resultado esperado. Horta i Camp concentra 64.188 unidades sin servir y cumple el 85,70 %.
-- La Cooperativa del Xúquer deja 4.670 unidades sin servir y cumple el 95,50 %.
-- Por qué. Agrupar por proveedor muestra dónde se concentra la brecha del producto. Antes de
-- atribuirle una causa, revisaríamos el volumen acordado, las entregas y la capacidad disponible.
SELECT s.supplier_name,
       SUM(m.requested_units) AS unidades_solicitadas,
       SUM(m.fulfilled_units) AS unidades_servidas,
       SUM(m.requested_units - m.fulfilled_units) AS unidades_sin_servir,
       ROUND(100.0 * SUM(m.fulfilled_units) / NULLIF(SUM(m.requested_units), 0), 2) AS cumplimiento_pct
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly` m
JOIN `PROJECT_ID.terra_taronja_raw.suppliers` s USING (supplier_id)
WHERE m.product_id = 1
  AND m.month_start >= DATE '2025-01-01' AND m.month_start < DATE '2026-01-01'
GROUP BY s.supplier_name
ORDER BY unidades_sin_servir DESC, s.supplier_name;

-- ¿Recomendaríais buscar nuevos proveedores y qué datos usaríais para justificarlo?
-- Resultado esperado. Consideraría un proveedor valenciano adicional para la naranja de Carcaixent.
-- Citaría las 68.858 unidades sin servir, el 87,54 % de cumplimiento y la brecha en los 12 meses.
-- Por qué. La repetición justifica revisar el suministro. Antes de contratar, comprobaría si los
-- proveedores actuales pueden cubrir más volumen y si el problema llega a afectar a los pedidos.

-- Ampliación para la puesta en común.

-- Bloque 1. ¿Qué productos acumulan más unidades solicitadas que quedaron sin servir?
-- Por qué. Restamos unidades servidas a unidades solicitadas para medir el faltante de
-- aprovisionamiento. Harían falta datos de pedidos de clientes sin atender para estimar ventas perdidas.
-- Interpretación. La naranja de Carcaixent encabeza el volumen sin servir. Conviene mirar los meses y el
-- proveedor antes de actuar.
SELECT p.product_name,
       SUM(m.requested_units) AS unidades_solicitadas,
       SUM(m.fulfilled_units) AS unidades_servidas,
       SUM(m.requested_units - m.fulfilled_units) AS unidades_sin_servir
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly` AS m
JOIN `PROJECT_ID.terra_taronja_raw.products` AS p USING (product_id)
WHERE m.month_start >= DATE '2025-01-01' AND m.month_start < DATE '2026-01-01'
GROUP BY p.product_name
ORDER BY unidades_sin_servir DESC, p.product_name;

-- Bloque 2. ¿En qué meses se repite ese problema y en cuáles parece puntual?
-- Por qué. Agrupamos por producto y mes para distinguir un problema recurrente de un pico aislado.
-- Dividir por las unidades solicitadas hace comparables meses de distinto volumen.
-- Interpretación. Un producto que aparece varios meses con un porcentaje alto merece más atención que
-- uno con un único pico.
SELECT p.product_name, m.month_start AS mes,
       SUM(m.requested_units - m.fulfilled_units) AS unidades_sin_servir,
       100.0 * SUM(m.requested_units - m.fulfilled_units)
         / NULLIF(SUM(m.requested_units), 0) AS pct_sin_servir
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly` m
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
WHERE m.month_start >= DATE '2025-01-01' AND m.month_start < DATE '2026-01-01'
GROUP BY p.product_name, m.month_start
ORDER BY p.product_name, mes;

-- Bloque 3. ¿Qué parte de las unidades vendidas de cada producto depende de su proveedor principal?
-- Por qué. Sumamos las líneas vendidas por producto y proveedor. La cuota sobre el total del mismo
-- producto mide su exposición a la fuente principal, incluso si ese proveedor vende muchos otros
-- productos.
-- Interpretación. La cuota se calcula sobre las unidades totales de ese producto. Horta i Camp concentra
-- cerca del 80 % de la naranja de Carcaixent.
WITH ventas_proveedor AS (
  SELECT i.product_id, p.product_name, s.supplier_id, s.supplier_name,
         SUM(i.quantity) AS unidades
  FROM `PROJECT_ID.terra_taronja_raw.orders` o
  JOIN `PROJECT_ID.terra_taronja_raw.order_items` i USING (order_id)
  JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
  JOIN `PROJECT_ID.terra_taronja_raw.suppliers` s USING (supplier_id)
  WHERE o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
  GROUP BY i.product_id, p.product_name, s.supplier_id, s.supplier_name
), clasificacion AS (
  SELECT product_name, supplier_name, unidades,
         SUM(unidades) OVER (PARTITION BY product_id) AS unidades_producto,
         ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY unidades DESC, supplier_id) AS posicion
  FROM ventas_proveedor
)
SELECT product_name, supplier_name, unidades,
       100.0 * unidades / NULLIF(unidades_producto, 0) AS pct_unidades_del_producto
FROM clasificacion
WHERE posicion = 1
ORDER BY pct_unidades_del_producto DESC, product_name;

-- Bloque 4. ¿Cómo se comparan los proveedores del mismo producto en retrasos, unidades recibidas y días de rotura?
-- Por qué. Comparar proveedores del mismo producto reduce diferencias de conservación y estacionalidad.
-- Medimos retrasos por expedición y recepción frente a lo planificado para tener en cuenta el volumen de
-- cada proveedor.
-- Interpretación. Leed el número de expediciones junto al porcentaje. Los días de rotura se acumulan
-- para cada pareja de producto y proveedor durante el año.
SELECT p.product_name, s.supplier_name,
       SUM(m.shipments) AS expediciones,
       100.0 * SUM(m.late_shipments) / NULLIF(SUM(m.shipments), 0) AS pct_tardias,
       SUM(m.received_units) AS unidades_recibidas,
       SUM(m.planned_units) AS unidades_planificadas,
       100.0 * SUM(m.received_units) / NULLIF(SUM(m.planned_units), 0) AS pct_recibidas,
       SUM(m.stockout_days) AS dias_rotura_acumulados
FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly` m
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
JOIN `PROJECT_ID.terra_taronja_raw.suppliers` s USING (supplier_id)
WHERE m.month_start >= DATE '2025-01-01' AND m.month_start < DATE '2026-01-01'
GROUP BY p.product_name, s.supplier_name
ORDER BY p.product_name, pct_tardias DESC, s.supplier_name;

-- Bloque 5. ¿Para qué productos tendría sentido incorporar otro proveedor y qué información necesitaríais antes de hacerlo?
-- Consulta avanzada de referencia.
-- Por qué. Cruzamos concentración, unidades sin servir y roturas porque cada indicador por separado
-- admite otras explicaciones. Si coinciden de forma persistente, una fuente alternativa con capacidad
-- disponible puede reducir el riesgo.
-- Interpretación. Priorizaría un proveedor valenciano adicional para la naranja de Carcaixent y
-- revisaría también la mandarina de Nules. Antes pediría datos de capacidad, plazos y costes a los
-- proveedores alternativos.
WITH sales AS (
  SELECT DATE_TRUNC(o.order_date, MONTH) AS month_start, i.product_id, i.supplier_id,
         SUM(i.quantity) AS sold_units
  FROM `PROJECT_ID.terra_taronja_raw.order_items` i
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
  WHERE o.order_date >= DATE '2025-01-01'
  GROUP BY 1, 2, 3
), monthly AS (
  SELECT m.*, p.product_name, s.supplier_name, COALESCE(v.sold_units, 0) AS sold_units
  FROM `PROJECT_ID.terra_taronja_raw.supplier_monthly` m
  JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
  JOIN `PROJECT_ID.terra_taronja_raw.suppliers` s USING (supplier_id)
  LEFT JOIN sales v USING (month_start, product_id, supplier_id)
  WHERE m.month_start >= DATE '2025-01-01'
)
SELECT product_name, supplier_name,
       SUM(sold_units) AS sold_units,
       1.0 * SUM(sold_units) /
         NULLIF(SUM(SUM(sold_units)) OVER (PARTITION BY product_id), 0) AS sales_share,
       SUM(requested_units - fulfilled_units) AS unserved_units,
       1.0 * SUM(requested_units - fulfilled_units) / NULLIF(SUM(requested_units), 0) AS unserved_share,
       1.0 * SUM(received_units) / NULLIF(SUM(planned_units), 0) AS fill_rate,
       1.0 * SUM(late_shipments) / NULLIF(SUM(shipments), 0) AS late_share,
       SUM(CASE WHEN stockout_days > 0 THEN 1 ELSE 0 END) AS months_with_stockouts,
       MIN(stockout_days) AS min_stockout_days,
       MAX(stockout_days) AS max_stockout_days
FROM monthly
GROUP BY product_id, product_name, supplier_name
ORDER BY unserved_units DESC;
