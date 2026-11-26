-- Sustituye PROJECT_ID y ejecuta con ubicación EU tras cargar orders.
CREATE SCHEMA IF NOT EXISTS `PROJECT_ID.terra_taronja_analitica`
OPTIONS (location = 'EU', default_table_expiration_days = 2);

CREATE OR REPLACE TABLE `PROJECT_ID.terra_taronja_analitica.orders_partitioned`
PARTITION BY DATE_TRUNC(order_date, MONTH)
AS
SELECT * FROM `PROJECT_ID.terra_taronja_raw.orders`;

CREATE OR REPLACE TABLE `PROJECT_ID.terra_taronja_analitica.orders_optimized`
PARTITION BY DATE_TRUNC(order_date, MONTH)
CLUSTER BY province, customer_type
AS
SELECT * FROM `PROJECT_ID.terra_taronja_raw.orders`;
