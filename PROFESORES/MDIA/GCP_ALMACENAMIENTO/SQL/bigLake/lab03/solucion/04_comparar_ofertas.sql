WITH ofertas AS (
  SELECT 'A' AS supplier_id, supplier_sku, product_name, price_eur, available_units
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_a`
  UNION ALL
  SELECT supplier_id, supplier_sku, product_name, price_eur, available_units
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur`
  UNION ALL
  SELECT 'C', article_ref, label, CAST(unit_price_eur AS NUMERIC), units_on_hand
  FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_c`
)
SELECT
  p.product_id,
  p.product_name AS producto,
  p.sales_unit AS unidad,
  o.supplier_id AS proveedor,
  o.price_eur AS precio_eur,
  o.available_units AS stock,
  o.available_units >= 50 AS cubre_50
FROM ofertas AS o
JOIN `TU_PROJECT_ID.terra_taronja_biglake.lab03_correspondencias` AS m
  ON o.supplier_id = m.supplier_id
  AND o.supplier_sku = m.supplier_sku
JOIN `TU_PROJECT_ID.terra_taronja_biglake.lab03_productos` AS p
  ON m.product_id = p.product_id
ORDER BY producto, cubre_50 DESC, precio_eur, stock DESC, proveedor;
