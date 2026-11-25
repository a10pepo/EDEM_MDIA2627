CREATE EXTERNAL TABLE `TU_PROJECT_ID.terra_taronja_biglake_a01.proveedor_b_biglake` (
  product_code STRING,
  description STRING,
  price_cents INT64,
  stock INT64
)
WITH CONNECTION `TU_PROJECT_ID.UBICACION.terra_taronja_restringida`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['URI_NDJSON']
);
