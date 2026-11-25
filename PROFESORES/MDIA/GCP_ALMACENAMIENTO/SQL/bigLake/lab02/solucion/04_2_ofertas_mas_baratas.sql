SELECT product_code,
       description,
       CAST(price_cents AS NUMERIC) / 100 AS precio_eur,
       stock
FROM `TU_PROJECT_ID.terra_taronja_biglake_a01.proveedor_b_biglake`
WHERE stock > 0
ORDER BY price_cents, product_code
LIMIT 3;
