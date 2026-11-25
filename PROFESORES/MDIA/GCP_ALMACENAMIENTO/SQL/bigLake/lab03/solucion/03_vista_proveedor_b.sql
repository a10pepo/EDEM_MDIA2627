CREATE OR REPLACE VIEW `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur` AS
SELECT
  'B' AS supplier_id,
  product_code AS supplier_sku,
  description AS product_name,
  CAST(price_cents AS NUMERIC) / 100 AS price_eur,
  stock AS available_units
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b`;

SELECT supplier_sku, product_name, price_eur, available_units
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b_eur`
WHERE supplier_sku = 'B-0135';
