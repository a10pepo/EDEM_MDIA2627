-- Sustituye PROJECT_ID por el ID del proyecto y ejecuta cada consulta por separado en EU.

-- Cifras de referencia para la escala completa con semilla 27182.

-- Cuando hay una sola consulta para varias preguntas, revisa sus columnas antes de pasar a la siguiente.

-- ¿Quién hizo más pedidos en 2025, los restaurantes o las grandes empresas (customer_type en orders)?
-- Resultado esperado. Los restaurantes hicieron 140.176 pedidos. Las grandes empresas hicieron 8.772.
-- Por qué. Contar filas mide el volumen de pedidos de cada grupo. La misma consulta calcula el importe
-- medio.
SELECT customer_type, COUNT(*) AS pedidos,
       ROUND(AVG(net_cents) / 100.0, 2) AS importe_neto_medio_eur
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
  AND customer_type IN ('restaurante', 'gran_empresa')
GROUP BY customer_type
ORDER BY pedidos DESC, customer_type;

-- ¿En qué grupo es mayor el importe neto medio por pedido (net_cents en céntimos)?
-- Resultado esperado. Las grandes empresas tienen el mayor importe neto medio, con 411,48 € por pedido
-- frente a 93,97 € de los restaurantes.
-- Por qué. La media por pedido permite comparar el tamaño de la compra aunque un grupo haga más pedidos.

-- ¿A qué grupo ofreceríais primero una prueba de venta a negocios y por qué?
-- Resultado esperado. Probaría primero con restaurantes por el volumen de pedidos. Las grandes empresas
-- aportan una cesta más grande, así que revisaría cuánto cuesta atender a cada grupo antes de elegir.
-- Por qué. El volumen y el tamaño del pedido sirven para plantear una prueba. La decisión comercial
-- necesita además información de costes y recurrencia.

-- ¿Qué os falta saber antes de decidir?
-- Resultado esperado. Miraría el coste de atender cada pedido, los descuentos, la frecuencia por cliente
-- y cuánto costaría captar y dar soporte a negocios.
-- Por qué. Estos datos permiten valorar cuánto conserva la tienda por venta y si el canal cubriría sus
-- gastos.

-- ¿Qué podéis mirar si os queda tiempo?

-- ¿Cuánto le cuesta de media a la tienda atender un pedido de cada grupo (service_cost_cents)?
-- Resultado esperado. Atender un pedido cuesta de media 1,89 € en restaurantes y 22,43 € en grandes
-- empresas.
-- Por qué. Dividir por pedido compara ambos grupos en la misma unidad.
SELECT customer_type,
       ROUND(AVG(service_cost_cents) / 100.0, 2) AS servicio_medio_eur,
       ROUND(100.0 * SUM(contribution_cents) / NULLIF(SUM(net_cents), 0), 1) AS contribucion_pct
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
  AND customer_type IN ('restaurante', 'gran_empresa')
GROUP BY customer_type
ORDER BY servicio_medio_eur, customer_type;

-- ¿Qué segmento deja más contribución por cada euro de venta neta?
-- Resultado esperado. Los restaurantes conservan un 28,9 % y las grandes empresas un 10,9 %.
-- Por qué. La columna contribucion_pct de la consulta anterior divide la contribución total
-- de cada grupo por sus ventas netas. Así comparamos lo que queda por cada euro vendido.

-- Ampliación para la puesta en común.

-- Bloque 1. ¿Cuántos clientes activos y pedidos hay en cada segmento y cuánto vale su cesta media?
-- Por qué. El recuento de clientes distintos separa el tamaño del segmento del número de pedidos. La
-- media por pedido permite comparar el valor de la cesta aunque los segmentos tengan bases muy
-- diferentes.
-- Interpretación. Las grandes empresas tienen la mayor cesta media. Los restaurantes reúnen más pedidos
-- en total que las grandes empresas.
SELECT customer_type,
       COUNT(DISTINCT customer_id) AS clientes_activos,
       COUNT(*) AS pedidos,
       AVG(net_cents) / 100.0 AS cesta_media_eur
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY customer_type
ORDER BY cesta_media_eur DESC;

-- Bloque 2. ¿Cómo compararíais cuántas veces compra un cliente dando a todos el mismo plazo desde su primera compra?
-- Por qué. Usamos 90 días desde la primera compra para que las cuentas antiguas no partan con ventaja.
-- Conservamos a quienes hicieron un único pedido porque también cuentan para medir la frecuencia.
-- Interpretación. El total medio incluye la primera compra. Los pedidos posteriores también permiten
-- calcular qué parte del segmento repite.
WITH seguimiento AS (
  SELECT c.customer_type, c.customer_id, COUNT(o.order_id) AS pedidos_posteriores
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
    ON o.customer_id = c.customer_id
   AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 1 AND 90
  WHERE c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
  GROUP BY c.customer_type, c.customer_id
)
SELECT customer_type, COUNT(*) AS clientes_con_90_dias,
       AVG(1.0 + pedidos_posteriores) AS pedidos_medios_90d,
       100.0 * AVG(CASE WHEN pedidos_posteriores > 0 THEN 1.0 ELSE 0.0 END) AS pct_repite_90d
FROM seguimiento
GROUP BY customer_type
ORDER BY pedidos_medios_90d DESC;

-- Bloque 3. ¿Cuánto representan los descuentos y cuánto cuesta atender un pedido en cada segmento?
-- Por qué. Medimos el descuento por euro bruto porque las cestas tienen importes distintos. Medimos el
-- servicio por pedido porque indica lo que cuesta atender una compra adicional en cada segmento.
-- Interpretación. El descuento es una proporción del bruto. El coste de servicio está en euros por
-- pedido y es mucho mayor en las grandes empresas.
SELECT customer_type,
       AVG(service_cost_cents) / 100.0 AS servicio_medio_eur,
       100.0 * SUM(discount_cents) / NULLIF(SUM(gross_cents), 0) AS pct_descuento,
       100.0 * SUM(contribution_cents) / NULLIF(SUM(net_cents), 0) AS pct_contribucion
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY customer_type
ORDER BY pct_contribucion DESC;

-- Bloque 4. ¿Qué segmento deja más contribución por cada euro de venta neta?
-- Por qué. Dividimos la contribución total por las ventas netas totales. Así cada pedido pesa según el
-- ingreso que aporta y los resultados incluyen los pedidos con contribución negativa.
-- Interpretación. Los particulares lideran por euro de venta neta. Los restaurantes quedan cerca y
-- superan claramente a las grandes empresas en este cociente.
SELECT customer_type,
       SUM(net_cents) / 100.0 AS ventas_netas_eur,
       SUM(contribution_cents) / 100.0 AS contribucion_eur,
       1.0 * SUM(contribution_cents) / NULLIF(SUM(net_cents), 0) AS contribucion_por_euro_neto
FROM `PROJECT_ID.terra_taronja_raw.orders`
WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
GROUP BY customer_type
ORDER BY contribucion_por_euro_neto DESC;

-- Bloque 5. ¿Qué diferencias encontráis entre clientes de un mismo segmento?
-- Por qué. Calculamos el resultado por cuenta antes de agrupar por segmento. Esto permite ver cuántas
-- cuentas pierden dinero en costes variables o superan un umbral que el promedio del segmento podría
-- ocultar.
-- Interpretación. La variación importa. Más del 22 % de las grandes cuentas activas supera el 20 % de
-- contribución sobre sus ventas netas.
WITH resultado_cliente AS (
  SELECT customer_type, customer_id,
         SUM(contribution_cents) AS contribucion_cents,
         1.0 * SUM(contribution_cents) / NULLIF(SUM(net_cents), 0) AS tasa_contribucion
  FROM `PROJECT_ID.terra_taronja_raw.orders`
  WHERE order_date >= DATE '2025-01-01' AND order_date < DATE '2026-01-01'
  GROUP BY customer_type, customer_id
)
SELECT customer_type, COUNT(*) AS clientes_activos,
       SUM(CASE WHEN contribucion_cents < 0 THEN 1 ELSE 0 END) AS clientes_con_perdida_variable,
       100.0 * AVG(CASE WHEN tasa_contribucion > 0.20 THEN 1.0 ELSE 0.0 END) AS pct_clientes_sobre_20,
       100.0 * MIN(tasa_contribucion) AS pct_minimo,
       100.0 * MAX(tasa_contribucion) AS pct_maximo
FROM resultado_cliente
GROUP BY customer_type
ORDER BY customer_type;

-- Bloque 6. ¿A qué segmento ofreceríais un piloto B2B y qué costes habría que estimar antes de lanzarlo?
-- Consulta avanzada de referencia.
-- Por qué. La recurrencia de los restaurantes da más ocasiones de recuperar los costes de captación y su
-- contribución por euro neto supera a la de las grandes empresas. El piloto debe comprobar si esto
-- cubre los costes de un canal dedicado.
-- Interpretación. Empezaría con pequeños restaurantes. Presupuestaría la captación, el soporte dedicado
-- y los costes fijos del canal.
WITH annual AS (
  SELECT customer_type, customer_id, COUNT(*) AS orders,
         SUM(net_cents) AS net_cents, SUM(contribution_cents) AS contribution_cents,
         SUM(service_cost_cents) AS service_cost_cents, SUM(discount_cents) AS discount_cents,
         SUM(gross_cents) AS gross_cents
  FROM `PROJECT_ID.terra_taronja_raw.orders`
  WHERE order_date >= DATE '2025-01-01'
  GROUP BY customer_type, customer_id
), followup AS (
  SELECT c.customer_type, c.customer_id, COUNT(o.order_id) AS repeat_orders
  FROM `PROJECT_ID.terra_taronja_raw.customers` c
  LEFT JOIN `PROJECT_ID.terra_taronja_raw.orders` o
    ON o.customer_id = c.customer_id
   AND DATE_DIFF(o.order_date, c.first_order_date, DAY) BETWEEN 1 AND 90
  WHERE c.first_order_date BETWEEN DATE '2025-01-01' AND DATE '2025-10-02'
  GROUP BY c.customer_type, c.customer_id
), frequencies AS (
  SELECT customer_type, COUNT(*) AS cohort_customers, AVG(1.0 + repeat_orders) AS orders_90d,
         AVG(CASE WHEN repeat_orders > 0 THEN 1.0 ELSE 0.0 END) AS repeat_90d
  FROM followup
  GROUP BY customer_type
)
SELECT a.customer_type, COUNT(*) AS active_customers, SUM(a.orders) AS orders,
       f.cohort_customers, f.orders_90d, f.repeat_90d,
       SUM(a.net_cents) / NULLIF(100.0 * SUM(a.orders), 0) AS basket_eur,
       SUM(a.service_cost_cents) / NULLIF(100.0 * SUM(a.orders), 0) AS service_eur,
       1.0 * SUM(a.discount_cents) / NULLIF(SUM(a.gross_cents), 0) AS discount_share,
       1.0 * SUM(a.contribution_cents) / NULLIF(SUM(a.net_cents), 0) AS contribution_rate,
       AVG(CASE WHEN a.contribution_cents > 0 THEN 1.0 ELSE 0.0 END) AS profitable_customer_share,
       AVG(CASE WHEN a.contribution_cents > 0.20 * a.net_cents THEN 1.0 ELSE 0.0 END) AS customer_share_over_20
FROM annual a
JOIN frequencies f USING (customer_type)
GROUP BY a.customer_type, f.cohort_customers, f.orders_90d, f.repeat_90d
ORDER BY a.customer_type;
