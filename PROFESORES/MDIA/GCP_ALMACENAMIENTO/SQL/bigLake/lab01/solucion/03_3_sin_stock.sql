SELECT supplier_sku, product_name
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`
WHERE available_units = 0
ORDER BY supplier_sku;
