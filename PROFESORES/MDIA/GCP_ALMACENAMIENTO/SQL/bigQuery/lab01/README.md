# BigQuery · Lab 1 · Las primeras ventas de Terra Taronja

**25 minutos · Trabajo individual · Google Cloud Console**

Terra Taronja vende exclusivamente productos alimentarios de la Comunitat Valenciana. Sus clientes pueden estar en otras provincias. Hoy abrirás una muestra de su histórico para descubrir qué se vende, cuándo y a qué destinos.

En Cloud SQL trabajaste con pedidos y transacciones. Aquí usarás BigQuery para buscar patrones en muchas ventas a la vez.

## Antes de empezar

- Entra en [BigQuery Studio](https://console.cloud.google.com/bigquery) con la cuenta de la clase. Selecciona tu proyecto GCP y apunta su **ID**, que puede ser distinto del nombre visible.
- Comprueba que tu proyecto tiene una cuenta de facturación vinculada y la API de BigQuery habilitada. Si te faltan permisos para crear el dataset, pide el rol **BigQuery User** en el proyecto. Al crear el dataset obtienes permisos sobre él. [Permisos de BigQuery](https://docs.cloud.google.com/bigquery/docs/access-control)
- Abre [ventas.csv](./datos/ventas.csv) y [ventas.schema.json](./datos/ventas.schema.json). Si estás en GitHub, usa **Download raw file** en la página de cada archivo. Conserva el CSV tal como se descarga, con la cabecera en la primera fila. [Descargar archivos desde GitHub](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files#viewing-or-copying-the-raw-file-content)

## 1. Crea un dataset · 5 min

En **Explorer**, expande tu proyecto, abre **Datasets** y pulsa **Create dataset**. En **Dataset ID** escribe `terra_taronja_lab01`. En **Location type** elige **Multi-region** y selecciona **EU**. Deja el resto con los valores por defecto y pulsa **Create dataset**.

El dataset agrupa tablas y fija dónde se guardan. En **Explorer** deberías ver `terra_taronja_lab01` debajo de tu proyecto. [Crear un dataset](https://docs.cloud.google.com/bigquery/docs/datasets)

## 2. Crea la tabla vacía · 5 min

Abre el dataset y pulsa **Create table**. En **Create table from** elige **Empty table**. En **Destination**, escribe `ventas` en el campo **Table**. En **Schema**, activa **Edit as text** y pega el contenido de [ventas.schema.json](./datos/ventas.schema.json). Deja la tabla sin particionar y pulsa **Create table**. [Crear una tabla](https://docs.cloud.google.com/bigquery/docs/tables)

Abre `ventas` y comprueba en **Schema** que aparecen las columnas. En **Details**, la tabla debe tener **0 filas**.

Cada fila representa un producto dentro de un pedido. Un pedido con tres productos ocupa tres filas, todas con el mismo `order_id`.

| Columna | Tipo | Qué representa |
| --- | --- | --- |
| `order_id` | INTEGER | Identificador del pedido |
| `order_date` | DATE | Fecha de compra |
| `province` | STRING | Provincia de destino |
| `product_name`, `category` | STRING | Producto y categoría |
| `origin_province` | STRING | Provincia valenciana de origen |
| `quantity` | INTEGER | Unidades pedidas en la línea |
| `unit_price_cents` | INTEGER | Precio unitario antes de descuentos |
| `line_net_cents` | INTEGER | Ingreso de la línea tras descuentos y devoluciones, en céntimos y sin portes |

## 3. Carga el CSV en la tabla existente · 5 min

BigQuery usa el formulario **Create table** también para importar archivos. En este paso el destino es la tabla `ventas` que acabas de crear.

1. Vuelve al dataset y pulsa **Create table**. En **Create table from** elige **Upload**, pulsa **Browse** y selecciona `ventas.csv`. En **File format** elige **CSV**.
2. En **Destination** indica tu **Project**, el **Dataset** `terra_taronja_lab01` y la **Table** `ventas`. Deja **Auto detect** desmarcado. Si el formulario te pide el esquema, usa **Edit as text** y pega el mismo JSON del paso 2.
3. En **Advanced options**, indica **1** en **Header rows to skip**, elige **Comma** en **Field delimiter** y mantén **UTF-8**. En **Write preference**, elige **Write if empty** para evitar duplicados si repites la carga. Si esa opción no aparece, usa **Append to table** solo después de comprobar en **Details** que `ventas` tiene 0 filas.
4. Pulsa **Create table** para iniciar la carga y espera a que termine. Si falla en la fila 1 o en `order_id`, revisa **Header rows to skip**. Si cargaste el mismo CSV dos veces, repite la carga una sola vez con **Overwrite table** tras comprobar que el destino es `terra_taronja_lab01.ventas`. [Carga de archivos locales](https://docs.cloud.google.com/bigquery/docs/batch-loading-data)

## 4. Abre la tabla y comprueba el resultado · 5 min

- **Schema**. Comprueba que `order_date` sea `DATE` y `quantity` sea `INTEGER`.
- **Preview**. Busca un pedido con varias líneas y compara el origen del producto con su destino.
- **Details**. Localiza el número de filas, el ID completo de la tabla y su tamaño de almacenamiento.
- Pulsa **SQL query**, pega la consulta y sustituye `PROJECT_ID` por el ID de tu proyecto. Pulsa **Run**. Si aparece un error de ubicación, revisa que el trabajo se ejecute en **EU** en **Edit → Query settings**. [Ejecutar consultas](https://docs.cloud.google.com/bigquery/docs/running-queries)

```sql
SELECT COUNT(*) AS lineas, COUNT(DISTINCT order_id) AS pedidos,
       MIN(order_date) AS primer_dia, MAX(order_date) AS ultimo_dia
FROM `PROJECT_ID.terra_taronja_lab01.ventas`;
```

Deberías ver **980 líneas**, **320 pedidos** y fechas del **7 de enero de 2023** al **30 de diciembre de 2025**.

## 5. Investiga la muestra · 5 min

Elige dos preguntas y anota qué columnas usaste para responder.

- ¿Cuántos pedidos de 2025 llegaron a cada provincia?
- ¿Qué tres productos movieron más unidades? ¿El orden cambia si miras el ingreso neto?
- ¿Qué provincias valencianas aparecen como origen? ¿A qué destinos llegaron sus productos?
- ¿Qué mes de 2025 tuvo más ingresos netos en la muestra?

Usa `COUNT(DISTINCT order_id)` si quieres contar pedidos y `SUM(line_net_cents) / 100.0` si quieres expresar ingresos en euros. Para todas las preguntas basta con la tabla `ventas`. Puedes abrir el [catálogo de 20 productos](./datos/products.csv) como referencia para consultar la localidad de origen o el precio de catálogo.

Puedes contrastar tus resultados con las [consultas resueltas](./solucion/consultas.sql).

## Limpieza

En **Explorer**, abre el proyecto, entra en **Datasets** y selecciona `terra_taronja_lab01`. Comprueba el proyecto y el nombre antes de pulsar **Delete**. En el diálogo **Delete dataset**, escribe `delete` y pulsa **Delete**. Verifica en **Explorer** que ya no aparece el dataset. Los siguientes ejercicios usan otros datasets. [Eliminar un dataset](https://docs.cloud.google.com/bigquery/docs/managing-datasets)
