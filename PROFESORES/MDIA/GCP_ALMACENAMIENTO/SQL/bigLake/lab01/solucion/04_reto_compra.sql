SELECT supplier_sku, product_name, price_eur, available_units
FROM `PROJECT_ID.terra_taronja_biglake.proveedor_a_ext`
WHERE available_units >= 50 AND price_eur <= 4
ORDER BY available_units DESC, supplier_sku
LIMIT 3;

-- Resultado esperado, de mayor a menor stock:
-- A-0149 | Limón de Orihuela      | 3,40 € | 159 unidades
-- A-0107 | Naranja de Carcaixent  | 3,65 € | 128 unidades
-- A-0114 | Arroz bomba de Sueca   | 3,81 € | 128 unidades
--
-- Presentaría primero el limón porque tiene el mayor stock entre las ofertas
-- que cumplen el presupuesto y la cantidad del pedido. La naranja y el arroz
-- empatan en stock y se ordenan por referencia.
--
-- Reflexión:
-- 1. El CSV está en Cloud Storage. La tabla externa guarda su ruta y esquema.
-- 2. El proveedor debe actualizar el precio en el CSV que lee la tabla.
-- 3. Antes de pedir, confirma la unidad comercial, los portes y el plazo de entrega.
