SELECT 'A' AS proveedor, 'CSV' AS formato, COUNT(*) AS ofertas
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_a`
UNION ALL
SELECT 'B', 'NDJSON', COUNT(*)
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_b`
UNION ALL
SELECT 'C', 'Parquet', COUNT(*)
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_proveedor_c`
ORDER BY proveedor;
