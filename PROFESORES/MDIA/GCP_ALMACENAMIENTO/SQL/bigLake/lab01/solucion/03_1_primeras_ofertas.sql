SELECT supplier_sku, product_name, price_eur, available_units
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`
ORDER BY supplier_sku
LIMIT 5;
