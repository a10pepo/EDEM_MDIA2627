-- Ejecuta esta consulta con el bloque de Cloud Shell del paso 5 para usar la cuenta de analista.
SELECT SESSION_USER() AS mi_cuenta, COUNT(*) AS ofertas
FROM `TU_PROJECT_ID.terra_taronja_biglake_a01.proveedor_b_biglake`;
