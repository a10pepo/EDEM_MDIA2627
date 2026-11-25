-- Alternativa para CSV en un bucket existente compatible con EU.
-- Sustituye PROJECT_ID y BUCKET_NAME. Ejecuta primero 01_crear_raw.sql.
-- OVERWRITE reemplaza el contenido de estas tablas didácticas.

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.customers` (
  customer_id INT64 NOT NULL,
  customer_type STRING NOT NULL,
  province STRING NOT NULL,
  region STRING NOT NULL,
  registered_date DATE NOT NULL,
  first_order_date DATE NOT NULL,
  customer_name STRING,
  email STRING
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/customers.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.orders` (
  order_id INT64 NOT NULL,
  order_date DATE NOT NULL,
  customer_id INT64 NOT NULL,
  customer_type STRING NOT NULL,
  province STRING NOT NULL,
  region STRING NOT NULL,
  campaign STRING NOT NULL,
  delivery_date DATE NOT NULL,
  delivery_incident BOOL NOT NULL,
  gross_cents INT64 NOT NULL,
  discount_cents INT64 NOT NULL,
  refund_cents INT64 NOT NULL,
  product_cost_cents INT64 NOT NULL,
  shipping_paid_cents INT64 NOT NULL,
  shipping_cost_cents INT64 NOT NULL,
  service_cost_cents INT64 NOT NULL,
  net_cents INT64 NOT NULL,
  contribution_cents INT64 NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/orders.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.order_items` (
  order_id INT64 NOT NULL,
  line_number INT64 NOT NULL,
  product_id INT64 NOT NULL,
  supplier_id INT64 NOT NULL,
  quantity INT64 NOT NULL,
  unit_price_cents INT64 NOT NULL,
  unit_cost_cents INT64 NOT NULL,
  discount_cents INT64 NOT NULL,
  returned_quantity INT64 NOT NULL,
  refund_cents INT64 NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/order_items.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.products` (
  product_id INT64 NOT NULL,
  product_name STRING NOT NULL,
  category STRING NOT NULL,
  origin_region STRING NOT NULL,
  origin_province STRING NOT NULL,
  origin_locality STRING NOT NULL,
  list_price_cents INT64 NOT NULL,
  catalog_since DATE NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/products.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.suppliers` (
  supplier_id INT64 NOT NULL,
  supplier_name STRING NOT NULL,
  origin_region STRING NOT NULL,
  province STRING NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/suppliers.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.supplier_monthly` (
  month_start DATE NOT NULL,
  product_id INT64 NOT NULL,
  supplier_id INT64 NOT NULL,
  requested_units INT64 NOT NULL,
  fulfilled_units INT64 NOT NULL,
  planned_units INT64 NOT NULL,
  received_units INT64 NOT NULL,
  shipments INT64 NOT NULL,
  late_shipments INT64 NOT NULL,
  stockout_days INT64 NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/supplier_monthly.csv'],
  skip_leading_rows = 1
);

LOAD DATA OVERWRITE `PROJECT_ID.terra_taronja_raw.territory_monthly` (
  month_start DATE NOT NULL,
  province STRING NOT NULL,
  region STRING NOT NULL,
  sales_program STRING NOT NULL,
  coverage_pct INT64 NOT NULL,
  qualified_contacts INT64 NOT NULL
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://BUCKET_NAME/bigquery/territory_monthly.csv'],
  skip_leading_rows = 1
);
