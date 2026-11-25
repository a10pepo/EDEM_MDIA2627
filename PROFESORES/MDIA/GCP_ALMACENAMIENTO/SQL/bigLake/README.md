# Datos de BigLake · Terra Taronja

Los precios y las ofertas son sintéticos. El catálogo conserva los 20 productos valencianos del [Lab 01 de BigQuery](../bigQuery/lab01/datos/products.csv). El stock corresponde al **30 de abril de 2026**. Un stock de cero indica que la oferta está agotada.

Mantén la carpeta `datos/` en el repositorio. Terraform sube sus seis archivos en el Lab 01 y vuelve a subir el NDJSON al bucket restringido del Lab 02. El Lab 03 consulta esos archivos desde BigQuery.

| Archivo | Filas | Contenido |
| --- | ---: | --- |
| [proveedor_a.csv](./datos/proveedor_a.csv) | 16 | Referencia, producto, precio en euros y unidades disponibles. |
| [proveedor_b.ndjson](./datos/proveedor_b.ndjson) | 16 | Referencia, descripción, precio entero en céntimos y stock. |
| [proveedor_c.parquet](./datos/proveedor_c.parquet) | 16 | Referencia, etiqueta, precio en euros como DECIMAL(10,2) y stock como INT64. |
| [products.csv](./datos/products.csv) | 20 | Catálogo interno con ID de producto, origen, categoría y unidad de venta. |
| [product_supplier_map.csv](./datos/product_supplier_map.csv) | 48 | Relación de `supplier_id` y `supplier_sku` con el `product_id` interno. |
| [deliveries.csv](./datos/deliveries.csv) | 72 | Entregas con referencia, fechas previstas y reales, y unidades solicitadas y recibidas. |

Usa la clave conjunta `supplier_id` y `supplier_sku` para relacionar ofertas y entregas con el catálogo. B llama `product_code` a su referencia y C la llama `article_ref`. `sales_unit` indica la presentación que comparten las ofertas del mismo producto. Los precios se expresan por esa unidad, antes de impuestos y transporte.

El histórico contiene 24 entregas por proveedor, de enero a abril de 2026. Una entrega se considera puntual si `delivered_date <= expected_date` y completa si `received_units = ordered_units`. Sobre 24 entregas, A tiene 16 puntuales y 22 completas, B tiene 18 y 16, y C tiene 22 y 23.

## Regenerar y validar los datos

Los seis archivos están incluidos para ejecutar los labs. Si necesitas regenerarlos, abre una terminal en la carpeta `SQL`, que contiene `bigLake`, y usa Python 3.10 o posterior.

```text
python -m pip install -r bigLake/requirements.txt
python -X utf8 bigLake/generar_datos.py
python -X utf8 bigLake/test_datos.py
```

El generador usa la semilla `27182` y lee el catálogo del Lab 01 de BigQuery. Con `--output RUTA` puedes generar una copia en otra carpeta. Para reproducir también los bytes del Parquet, usa la misma versión de PyArrow. Las pruebas validan los archivos y ejecutan las soluciones del Lab 01 de BigLake en SQLite.
