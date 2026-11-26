-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado en EU.

-- Cifras de referencia para la escala completa con semilla 27182.
-- Si elegís otra categoría de comparación, ajustad las categorías y el periodo común.

-- Cuando hay una sola consulta para varias preguntas, revisa sus columnas antes de pasar a la siguiente.

-- ¿Cuándo apareció el primer producto de cada categoría en nuestro catálogo?
-- Resultado esperado. Aceites y miel, Bebidas, Cítricos y Despensa empezaron el 1 de enero de 2023.
-- Conservas vegetales empezó el 1 de abril de 2025. Dulces artesanos, el 1 de septiembre de 2025.
-- Por qué. La primera fecha de producto es el inicio de la categoría. La consulta también permite
-- responder a las dos preguntas siguientes.
SELECT category, MIN(catalog_since) AS primer_producto
FROM `PROJECT_ID.terra_taronja_raw.products`
GROUP BY category
ORDER BY primer_producto DESC, category;

-- ¿Qué categoría se incorporó más recientemente?
-- Resultado esperado. Dulces artesanos empezó más tarde, el 1 de septiembre de 2025.
-- Por qué. La primera fila de la consulta anterior contiene la fecha de lanzamiento más reciente.

-- ¿Con qué otra categoría la compararíais y desde qué mes estaban ambas presentes en el catálogo?
-- Resultado esperado. Compararía Dulces artesanos con Despensa entre septiembre y diciembre de 2025,
-- cuando ambas estaban en el catálogo.
-- Por qué. Comparar los mismos meses evita dar ventaja a la categoría más antigua por llevar más tiempo
-- a la venta.

-- ¿Cuántos pedidos incluyeron productos de cada categoría durante ese periodo común?
-- Resultado esperado. Entre septiembre y diciembre de 2025, 54.223 pedidos incluyeron Dulces artesanos
-- y 118.421 incluyeron Despensa.
-- Por qué. orders aporta la fecha y products la categoría de cada línea de order_items.
-- COUNT(DISTINCT i.order_id) cuenta una vez cada pedido dentro de cada categoría.
SELECT p.category, COUNT(DISTINCT i.order_id) AS pedidos
FROM `PROJECT_ID.terra_taronja_raw.order_items` i
JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
  AND p.category IN ('Dulces artesanos', 'Despensa')
GROUP BY p.category
ORDER BY pedidos DESC, p.category;

-- ¿Cuántos productos tenía cada categoría? ¿Cambia esto vuestra interpretación del número de pedidos?
-- Resultado esperado. Al cierre de diciembre, Dulces artesanos tenía 3 productos y Despensa, 4.
-- Despensa tenía una referencia más y, por tanto, más oportunidades de aparecer en un pedido.
-- Por qué. Contamos el catálogo, incluidos los productos sin pedidos. Para saber qué productos
-- tuvieron más aceptación, habría que mirar sus ventas y cuánto tiempo estuvieron disponibles.
SELECT category, COUNT(*) AS productos_en_catalogo
FROM `PROJECT_ID.terra_taronja_raw.products`
WHERE catalog_since < DATE '2026-01-01'
  AND category IN ('Dulces artesanos', 'Despensa')
GROUP BY category
ORDER BY category;

-- ¿Recomendaríais incorporar más productos de la categoría reciente o todavía faltan datos para tomar esa decisión?
-- Resultado esperado. Aplazaría la ampliación. Dulces artesanos aparece en 54.223 pedidos con
-- 3 productos durante el periodo. Antes mediría margen, devoluciones y pedidos fuera de Navidad.
-- Por qué. Los pedidos indican presencia en la cesta. Para ampliar interesa saber si las ventas
-- dejan margen y se mantienen cuando terminan las campañas.

-- ¿Qué podéis mirar si os queda tiempo?

-- ¿Cómo evolucionaron los pedidos mensuales de ambas categorías durante el periodo compartido?
-- Resultado esperado. De septiembre a diciembre, Dulces artesanos registra 6.395, 10.982, 16.774
-- y 20.072 pedidos. Despensa registra 29.281, 29.749, 28.610 y 30.781.
-- Por qué. La evolución mensual permite ver si el interés crece o se concentra al final del año.
SELECT DATE_TRUNC(o.order_date, MONTH) AS mes, p.category,
       COUNT(DISTINCT i.order_id) AS pedidos
FROM `PROJECT_ID.terra_taronja_raw.order_items` i
JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
  AND p.category IN ('Dulces artesanos', 'Despensa')
GROUP BY mes, p.category
ORDER BY mes, p.category;

-- Ampliación para la puesta en común.

-- Bloque 1. ¿Cuándo entró cada categoría en el catálogo y qué meses os permiten compararlas?
-- Por qué. La primera fecha de catálogo de un producto marca cuándo empieza a estar disponible su
-- categoría. La fecha de lanzamiento más reciente fija el primer mes compartido para la comparación.
-- Interpretación. La categoría más reciente entra en septiembre de 2025. La ventana común abarca
-- septiembre a diciembre.
WITH lanzamientos AS (
  SELECT category, MIN(catalog_since) AS primer_producto
  FROM `PROJECT_ID.terra_taronja_raw.products`
  GROUP BY category
)
SELECT category, primer_producto,
       DATE_TRUNC(MAX(primer_producto) OVER (), MONTH) AS inicio_mes_comun
FROM lanzamientos
ORDER BY primer_producto, category;

-- Bloque 2. ¿Cómo evolucionó el número de pedidos que incluían productos de cada categoría?
-- Por qué. Contamos pedidos distintos porque un pedido con varias líneas de una categoría debe contar
-- una vez en ella. Agrupar por mes permite observar cambios alrededor de campañas o lanzamientos.
-- Interpretación. Un pedido puede contar en varias categorías. Dulces artesanos muestra el mayor
-- crecimiento relativo entre septiembre y diciembre.
SELECT DATE_TRUNC(o.order_date, MONTH) AS mes, p.category,
       COUNT(DISTINCT i.order_id) AS pedidos
FROM `PROJECT_ID.terra_taronja_raw.order_items` AS i
JOIN `PROJECT_ID.terra_taronja_raw.orders` AS o USING (order_id)
JOIN `PROJECT_ID.terra_taronja_raw.products` AS p USING (product_id)
WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
GROUP BY mes, p.category
ORDER BY p.category, mes;

-- Bloque 3. ¿Qué parte de los pedidos coincidió con campañas y cuánto descuento se aplicó?
-- Por qué. Contamos campañas al nivel del pedido y sumamos descuentos al nivel de la línea. Dividir el
-- descuento total por el bruto total mide cuánto ingreso se cede en relación con el volumen vendido.
-- Interpretación. La coincidencia de compras y campañas señala dónde investigar. Para estimar el efecto
-- de una campaña hace falta una comparación controlada.
SELECT DATE_TRUNC(o.order_date, MONTH) AS mes, p.category,
       COUNT(DISTINCT o.order_id) AS pedidos,
       COUNT(DISTINCT CASE WHEN o.campaign <> 'sin_campana' THEN o.order_id END) AS pedidos_en_campana,
       100.0 * COUNT(DISTINCT CASE WHEN o.campaign <> 'sin_campana' THEN o.order_id END)
         / NULLIF(COUNT(DISTINCT o.order_id), 0) AS pct_pedidos_en_campana,
       SUM(i.discount_cents) / 100.0 AS descuento_eur,
       100.0 * SUM(i.discount_cents) / NULLIF(SUM(i.quantity * i.unit_price_cents), 0) AS pct_descuento
FROM `PROJECT_ID.terra_taronja_raw.order_items` i
JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
GROUP BY mes, p.category
ORDER BY mes, p.category;

-- Bloque 4. ¿Qué categorías tuvieron más devoluciones en proporción a las unidades vendidas?
-- Por qué. Dividimos las unidades devueltas entre las vendidas de cada categoría. El volumen por sí solo
-- puede hacer que una categoría parezca problemática aunque tenga pocas devoluciones por unidad.
-- Interpretación. Conservas vegetales destaca por la proporción de unidades devueltas en la misma
-- ventana de observación.
SELECT p.category, SUM(i.quantity) AS unidades_vendidas,
       SUM(i.returned_quantity) AS unidades_devueltas,
       100.0 * SUM(i.returned_quantity) / NULLIF(SUM(i.quantity), 0) AS pct_unidades_devueltas
FROM `PROJECT_ID.terra_taronja_raw.order_items` i
JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
GROUP BY p.category
ORDER BY pct_unidades_devueltas DESC, p.category;

-- Bloque 5. ¿Qué margen queda después de restar el coste del producto a los ingresos netos?
-- Por qué. Restamos descuentos y devoluciones para obtener el ingreso neto antes de descontar el coste
-- de producto. Expresar el margen sobre ese neto permite comparar categorías de distinto tamaño.
-- Interpretación. La cifra es margen de producto. En una decisión de ampliación todavía habría que tener
-- en cuenta logística y servicio.
WITH importes AS (
  SELECT p.category,
         SUM(i.quantity * i.unit_price_cents - i.discount_cents - i.refund_cents) AS neto_cents,
         SUM(i.quantity * i.unit_cost_cents) AS coste_cents
  FROM `PROJECT_ID.terra_taronja_raw.order_items` i
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
  JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
  WHERE o.order_date >= DATE '2025-09-01' AND o.order_date < DATE '2026-01-01'
  GROUP BY p.category
)
SELECT category, neto_cents / 100.0 AS neto_eur,
       (neto_cents - coste_cents) / 100.0 AS margen_producto_eur,
       100.0 * (neto_cents - coste_cents) / NULLIF(neto_cents, 0) AS pct_margen_producto
FROM importes
ORDER BY pct_margen_producto DESC, category;

-- Bloque 6. ¿Qué prueba haríais antes de decidir si ampliar, mantener o reducir alguna categoría?
-- Consulta avanzada de referencia.
-- Por qué. Un pico navideño puede ser estacional y un descuento puede elevar pedidos a costa del margen.
-- Un periodo fuera de campaña o una prueba con promociones comparables permite distinguir esas
-- explicaciones.
-- Interpretación. Probaría Dulces artesanos fuera de Navidad y observaría Conservas con incentivos
-- comparables. Para esta última, mediría devoluciones y margen bajo dos condiciones de promoción.
WITH category_month AS (
  SELECT DATE_TRUNC(o.order_date, MONTH) AS month_start, p.category,
         MIN(p.catalog_since) AS launch_date,
         COUNT(DISTINCT o.order_id) AS orders,
         COUNT(DISTINCT CASE WHEN o.campaign <> 'sin_campana' THEN o.order_id END) AS campaign_orders,
         SUM(i.quantity) AS units, SUM(i.returned_quantity) AS returned_units,
         SUM(i.quantity * i.unit_price_cents) AS gross_cents,
         SUM(i.discount_cents) AS discount_cents,
         SUM(i.refund_cents) AS refund_cents,
         SUM(i.quantity * i.unit_cost_cents) AS cost_cents
  FROM `PROJECT_ID.terra_taronja_raw.order_items` i
  JOIN `PROJECT_ID.terra_taronja_raw.orders` o USING (order_id)
  JOIN `PROJECT_ID.terra_taronja_raw.products` p USING (product_id)
  WHERE o.order_date >= DATE '2025-09-01'
  GROUP BY 1, 2
)
SELECT month_start, category, launch_date, orders, units,
       gross_cents - discount_cents - refund_cents AS net_cents,
       cost_cents,
       1.0 * campaign_orders / NULLIF(orders, 0) AS campaign_order_share,
       1.0 * discount_cents / NULLIF(gross_cents, 0) AS discount_share,
       1.0 * returned_units / NULLIF(units, 0) AS return_share,
       1.0 - 1.0 * cost_cents / NULLIF(gross_cents - discount_cents - refund_cents, 0) AS product_margin
FROM category_month
ORDER BY category, month_start;
