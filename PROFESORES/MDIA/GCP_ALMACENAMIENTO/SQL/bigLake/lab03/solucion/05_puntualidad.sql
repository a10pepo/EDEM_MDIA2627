SELECT
  supplier_id AS proveedor,
  COUNT(*) AS entregas,
  COUNTIF(delivered_date <= expected_date) AS a_tiempo,
  ROUND(100 * SAFE_DIVIDE(COUNTIF(delivered_date <= expected_date), COUNT(*)), 1) AS porcentaje
FROM `TU_PROJECT_ID.terra_taronja_biglake.lab03_entregas`
GROUP BY proveedor
ORDER BY proveedor;
