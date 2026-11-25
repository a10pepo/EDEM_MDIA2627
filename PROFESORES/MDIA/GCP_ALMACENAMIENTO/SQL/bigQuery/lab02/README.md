# BigQuery · Lab 2 · Consultas a escala

Terra Taronja vende productos de origen valenciano a distintos territorios. Trabaja en **tu propio proyecto GCP**, como en el Lab 1. Vas a crear dos datasets en **EU**, cargar el histórico y comparar cuatro formas de consultar los mismos pedidos.

## Antes de empezar

- Usa un proyecto con facturación vinculada y la API de BigQuery habilitada. Anota el **Project ID** y úsalo en lugar de `PROJECT_ID` en todos los SQL de la práctica. Si te faltan permisos para crear los datasets, pide el rol **BigQuery User** en tu proyecto. [Permisos de BigQuery](https://docs.cloud.google.com/bigquery/docs/access-control)
- Abre una terminal en la carpeta `SQL`, que contiene `bigQuery`. Usa esa misma carpeta para generar y cargar los CSV. Necesitas Python 3.10 o posterior y el comando `bq` de Google Cloud CLI. Si aún no has iniciado sesión en la CLI, ejecuta `gcloud auth login` con la misma cuenta que usas en la consola. [Instalar Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install) · [Iniciar sesión en la CLI](https://docs.cloud.google.com/sdk/docs/authenticate)

## 1. Genera los CSV

```text
python -X utf8 bigQuery/generar_datos.py --output bigQuery/salida
```

Usa `python3` si es el nombre del comando en tu equipo. Al terminar tendrás siete CSV en `bigQuery/salida`, con **1.200.000 pedidos** y **3.635.172 líneas de pedido**. Por ahora los archivos están en tu equipo.

## 2. Crea el dataset y las tablas vacías

En BigQuery Studio, selecciona tu proyecto y pulsa **SQL query**. Pega todo el contenido de [01_crear_raw.sql](./sql/01_crear_raw.sql), sustituye `PROJECT_ID` y selecciona **EU** como ubicación del trabajo en **Edit → Query settings**. Pulsa **Run**. En **Explorer** deben aparecer el dataset `terra_taronja_raw` y sus siete tablas vacías.

## 3. Carga los siete CSV

Vuelve a la terminal. Usa el bloque de tu sistema y sustituye `TU_PROJECT_ID` por el mismo ID que usaste en el SQL.

**PowerShell (Windows)**

```powershell
$projectBQ = 'TU_PROJECT_ID'
$tablesBQ = @('customers', 'orders', 'order_items', 'products', 'suppliers',
              'supplier_monthly', 'territory_monthly')

foreach ($tableBQ in $tablesBQ) {
    bq --project_id=$projectBQ --location=EU load --source_format=CSV --skip_leading_rows=1 --autodetect=false --replace=true "${projectBQ}:terra_taronja_raw.${tableBQ}" "bigQuery/salida/${tableBQ}.csv"
    if ($LASTEXITCODE -ne 0) { throw "Falló la carga de $tableBQ" }
}
```

**Bash (macOS o Linux)**

```bash
(
  set -e
  project_bq='TU_PROJECT_ID'
  for table_bq in customers orders order_items products suppliers supplier_monthly territory_monthly; do
    bq --project_id="$project_bq" --location=EU load \
      --source_format=CSV --skip_leading_rows=1 --autodetect=false --replace=true \
      "${project_bq}:terra_taronja_raw.${table_bq}" "bigQuery/salida/${table_bq}.csv"
  done
)
```

Cada carga reutiliza el esquema de su tabla. `--skip_leading_rows=1` omite la cabecera del CSV y `--replace=true` reemplaza los datos de esa tabla de práctica si repites la carga. Espera a que finalicen las siete. En **Explorer → terra_taronja_raw → orders → Details**, comprueba que hay **1.200.000 filas**. [Carga con bq](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference#bq_load)

### Si ya cargaste el Lab 2 antes de añadir nombre y correo

Vuelve a generar los CSV con la misma semilla y escala de tu carga anterior. Ejecuta de nuevo [01_crear_raw.sql](./sql/01_crear_raw.sql) con tu **Project ID** para añadir las columnas a `customers`. Después basta con recargar esa tabla. Sustituye `TU_PROJECT_ID` en los dos sitios del comando. [Añadir columnas en BigQuery](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas)

```text
bq --project_id=TU_PROJECT_ID --location=EU load --source_format=CSV --skip_leading_rows=1 --autodetect=false --replace=true "TU_PROJECT_ID:terra_taronja_raw.customers" "bigQuery/salida/customers.csv"
```

Abre **Preview** de `customers` y comprueba que aparecen `customer_name` y `email` con datos.

## 4. Crea las tablas de comparación

En BigQuery Studio, abre **SQL query** y ejecuta [03_crear_optimizada.sql](./sql/03_crear_optimizada.sql) con tu **Project ID** y ubicación **EU**. El script crea `terra_taronja_analitica` y copia los pedidos en dos tablas.

| Tabla | Cómo se organiza |
| --- | --- |
| `terra_taronja_raw.orders` | Tabla original |
| `terra_taronja_analitica.orders_partitioned` | Particiones por mes de `order_date` |
| `terra_taronja_analitica.orders_optimized` | Las mismas particiones y clustering por `province` y `customer_type` |

Comprueba en **Details** que las tres tablas de pedidos tienen **1.200.000 filas**. En las dos copias también debe figurar el particionado mensual.

## 5. Compara cuatro ejecuciones

1. Abre [04_comparar.sql](sql/04_comparar.sql) y sustituye `PROJECT_ID`. En BigQuery, pulsa **SQL query**. Abre **Edit → Query settings** y desmarca **Use cached results**. Ejecuta las cuatro consultas por separado con **Run**. [Caché de resultados](https://docs.cloud.google.com/bigquery/docs/cached-results)
2. Apunta el número de filas en **Results** y los bytes procesados, bytes facturados y duración en la información del trabajo. Con los datos generados en el paso 1, las cuatro consultas devuelven **7.339 filas**.
3. Compara **1 → 2** para aislar las columnas leídas, **2 → 3** para aislar el particionado y **3 → 4** para aislar el clustering. El filtro es el mismo. El particionado permite saltarse meses y el clustering puede saltarse bloques dentro de un mes. En particiones pequeñas es posible que las dos últimas consultas lean los mismos bytes.

El tiempo depende también de las condiciones de ejecución. Los bytes procesados suelen ser una medida más útil para esta comparación. `LIMIT` controla cuántas filas recibes. En la tabla raw sin clustering, por sí solo no reduce lo que se lee. [Configuración de consultas](https://docs.cloud.google.com/bigquery/docs/running-queries) · [Tablas particionadas](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables) · [Clustering](https://docs.cloud.google.com/bigquery/docs/clustered-tables)

Para comprobar los totales de la carga y ensayar una comparación adicional de clustering, abre [comprobaciones.sql](./solucion/comprobaciones.sql). La comparación adicional es opcional y crea otra tabla en `terra_taronja_analitica`.

## Limpieza

Si vas a hacer el [ejercicio final](../ejercicio_final/README.md), conserva `terra_taronja_raw` hasta que lo completes. Puedes eliminar `terra_taronja_analitica` en cuanto termines la comparación del Lab 2.

Para eliminar un dataset, abre **Explorer → Datasets** en tu proyecto y selecciona `terra_taronja_raw` o `terra_taronja_analitica`. Pulsa **Delete**, escribe `delete` en el diálogo y confirma con **Delete**. Comprueba que el dataset desaparece de **Explorer**. [Eliminar un dataset](https://docs.cloud.google.com/bigquery/docs/managing-datasets)
